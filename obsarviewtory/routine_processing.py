import os
import shutil
import subprocess
import tempfile
import time

from concurrent.futures import ProcessPoolExecutor
from datetime import date, timedelta, datetime

from osgeo import gdal
from osgeo_utils.gdal_merge import main as merge

try:
    # When run as a module
    from . import config, avo_insar_functions
except ImportError:
    # When run as a script
    import config, avo_insar_functions


import hyp3_sdk as sdk
from pathlib import Path
from mintpy.cli.smallbaselineApp import main as smallbaselineApp

class InSARProcessor:
    def __init__(self):
        """
        InSARProcessor __init__

        Create a hyp3 connection object, and the various paths and directories needed for InSAR
        processing.
        """
        #hyp3 = sdk.HyP3('https://hyp3-avo.asf.alaska.edu', prompt=True, username='ycheng', password='earthdata+1S')
        self.hyp3 = sdk.HyP3(prompt=True, username='ycheng', password='earthdata+1S')

        # List of succesfull and failed volcanoes/paths
        self.succesfull = []
        self.failed = []

        # Top level directory to store the processing directories in
        self.processing_dir = Path(__file__).parent / 'processings'

        # Directory to store the output InSAR products in
        self.product_dir = Path(os.path.dirname(__file__),  'products')

        # Use a temporary directory to store the downloaded files, so we only have to download
        # once per asf_name. The downloaded files will be copied into the processing directory
        # Directory will be automatically removed when class is destroyed.
        self._download_dir = tempfile.TemporaryDirectory()
        self.download_dir = Path(self._download_dir.name)

    def run(self):
        """
        Shortcut function to update the projects and generate products for all
        volcanoes
        """
        self.update_projects()
        self.process_volcanoes()

    def update_projects(self):
        """
        Update the projects at ASF, and mark any volcanoes associated with updated projects
        """
        watch_name = None

        for asf_project in config.asf_list:
            # TODO: if something dies before processing, this returns an up-to-date flag
            asf_flag = avo_insar_functions.update_asf_project(
                asf_project.path,
                asf_project.frame,
                asf_project.asf_name,
                self.hyp3
            ) # this function checks updates AND submit requests to ASF

            ###########DEBUG######
            if asf_flag == 0:
                asf_flag = 1
            ######################

            if asf_flag > 0:
                # We requested an update of something, so mark that we need to watch for it to finish.
                watch_name = asf_project.asf_name
                # We only need to run this if the flag is 1, since the flag defaults to 0
                for volc in config.volc_lookup[asf_project.asf_name]:
                    volc.update_flag(asf_flag)

            elif asf_flag == -1:
                # Mark volcanoes associated with this project as "failed", since we were unable
                # to check or update the associated ASF project.
                for volc in config.volc_lookup[asf_project.asf_name]:
                    self.failed.append(f"{volc.volc_name} - {volc.asf_name}: Unable to check/update ASF project")

        if watch_name is not None:
            jobs = self.hyp3.find_jobs(name=watch_name)
            jobs = self.hyp3.watch(jobs) # wait until asf has processed all submitted requests. May be several hours.


    def process_volcanoes(self):
        # Clean and re-create the output directory before starting the run.
        shutil.rmtree(str(self.product_dir), ignore_errors = True)
        self.product_dir.mkdir(parents = True, exist_ok = True)
        insar_dir = self.product_dir / 'insar'
        insar_dir.mkdir(exist_ok = True)

        processings = []

        # Run volcanoes in parallel
        with ProcessPoolExecutor() as executor:
            for volcano in config.volcano_list:
                if volcano.run_flag != 1:
                    continue

                proj_downloads: Path = self.download_dir / volcano.asf_name
                self.ensure_downloads(volcano, proj_downloads)

                # The following commented lines are if not running in parallel, the rest of
                # the function is for when parallel processing is desired
                # Pick one or the other, not both :)

                #-------- Single processing ---------------#
                #success,result = self.run_mintpy(volcano, proj_downloads)
                # if success:
                    # self.succesfull.append(result)
                # else:
                    # self.failed.append(result)
                #---------End Single Processing-------------#

            #---------Parallel Processing --------------#
                future = executor.submit(self.run_mintpy, volcano, proj_downloads)
                processings.append(future)

            for future in processings:
                success, result = future.result()
                if success:
                    self.succesfull.append(result)
                else:
                    self.failed.append(result)
            #------------End Parallel Processing ----------#


    def ensure_downloads(self, volcano, proj_downloads):
        if not proj_downloads.exists():
            print(f"Downloading files for {volcano.asf_name}")
            avo_insar_functions.avo_insar_download(
                self.hyp3,
                volcano.asf_name,
                proj_downloads,
                volcano.filter_dates
            )

            # Grab any interferograms from this download
            self.grab_ifg(volcano, proj_downloads)
        else:
            print(f"Files for {volcano.asf_name} already downloaded. Skipping download.")

    def grab_ifg(self, volcano, proj_downloads):
        path_frame = f"path{volcano.path}frame{volcano.frame}"
        kml_dir = self.product_dir / 'kml' / path_frame

        for f in proj_downloads.glob('S1*/*color_phase.kmz'):
            file_date = f.name[5:13] + '_' + f.name[21:29]
            date_dir: Path = kml_dir / file_date
            date_dir.mkdir(parents = True, exist_ok = True)
            shutil.copy(f, date_dir)


    def run_mintpy(self, volcano, proj_downloads):
        # Make sure we're in a good directory so MintPy doesn't fail (seriously???)
        os.chdir(self.processing_dir)

        print('########CURRENT PROJECT########')
        project_name = volcano.volc_name + str(volcano.path)
        analysis_directory: Path =  self.processing_dir / project_name
        mintpy_directory = analysis_directory / 'MintPy'

        print(f"analysis_directory: {analysis_directory}")

        # Initalize to default of success. We're optimistic here!
        success = True
        result_string = f"{volcano.volc_name} - {volcano.asf_name}"

        # Remove any existing processing directories. Leaving them can cause issues with leftover
        # files from previous runs.
        shutil.rmtree(analysis_directory, ignore_errors = True)

        # Copy the download files into the analysis_directory
        # Much faster than downloading again if we already have them downloaded.
        for f in proj_downloads.glob('*'):
            shutil.copytree(f, analysis_directory/f.name, dirs_exist_ok = True)

        merge_paths = list(analysis_directory.glob(f'*/*_amp.tif'))

        if not merge_paths:
            print(f"No images found for {volcano.volc_name}")
            return # No data for this volcano

        full_scene = analysis_directory/"full_scene.tif" # create a full scene for cropping
        merge_args = ['gdal_merge.py','-o', str(full_scene)] + [str(x) for x in merge_paths]
        merge(merge_args)

        # Create the vrt image
        image_file = f"{analysis_directory}/raster_stack.vrt"
        vrt_options = gdal.BuildVRTOptions(separate = True)
        gdal.BuildVRT(image_file, [str(full_scene), ], options = vrt_options)

        # Crop the image to the volcano area
        avo_insar_functions.avo_insar_crop(image_file, volcano.ul, volcano.lr, analysis_directory)

        # Create a config file for MintPy and return the path to said file
        mintpy_config = avo_insar_functions.avo_insar_run( analysis_directory , mintpy_directory )

        # Run MintPy, keeping track of success and failure
        app_args = ['--dir', str(mintpy_directory), str(mintpy_config)]
        try:
            smallbaselineApp(app_args)
        except Exception as e:
            success = False
            result_string = f"{volcano.volc_name} - {volcano.asf_name}: {e}"
        else:
            # Yay, it worked!
            #Move the products to the output directory
            output_ident = f"{volcano.volc_name.lower().replace(' ', '')}_main_path{volcano.path}.h5"
            for product in ('timeseries_ERA5_demErr', 'velocity'):
                dest = product.split('_')[0]
                shutil.move(str(mintpy_directory / f"{product}.h5"),
                            str(self.product_dir/ 'insar' / f"{dest}_{output_ident}") )

        # remove the processing directory
        shutil.rmtree(str(analysis_directory), ignore_errors = True)
        return (success, result_string)

    def upload_files(self):
        src = str(self.product_dir) + "/"
        dst = 'geodesy@apps.avo.alaska.edu:/geodesy/data/test/'
        dst_port = 2200
        key_file = os.path.join(os.path.dirname(__file__), 'id_rsa')
        cmd = ['rsync', '-r', '--stats', '-e', f'ssh -i {key_file} -p {dst_port}', src, dst]
        result = subprocess.run(cmd)
        if result.stdout:
            print(result.stdout)
        if result.stderr:
            print(result.stderr)


if __name__ == "__main__":
    t_start = time.time()
    print(f"Run starts at {datetime.now().strftime('%m/%d/%y %H:%M')}")

    processor = InSARProcessor()
    processor.run()
    processor.upload_files()

    print("")
    print("##################################################")

    runtime = time.time() - t_start
    units = "seconds"
    if runtime > 60:
        runtime /= 60
        units = "Minutes"
    if runtime > 60:
        runtime /= 60
        units = "Hours"

    runtime = round(runtime, 2)
    print(f"Run took {runtime} {units}")
    print("Failed generating files for:")
    for f in processor.failed:
        print(" - ", f)

    print('-------------------')
    print("Succesfully generated files for:")
    for s in processor.succesfull:
        print(" - ", s)
    print("#################################################")
    print(f"Run complete at {datetime.now().strftime('%m/%d/%y %H:%M')}")
