"""Main processing code for the AVO ObSARViewtory processing

This script will run the InSAR and interferogram processing for all
volcanoes and ASF projects listed in the config.py file.

This script can also be imported as a module.

Classes
-------
InSARProcessor
    The main class containing the processing code for InSAR data
"""

import os
import shutil
import subprocess
import tempfile
import time

from concurrent.futures import ProcessPoolExecutor
from datetime import datetime

from osgeo import gdal
from osgeo_utils.gdal_merge import gdal_merge

try:
    # When run as a module
    from . import config, avo_insar_functions
except ImportError:
    # When run as a script
    import avo_insar_functions
    import config


import hyp3_sdk as sdk
from pathlib import Path
from mintpy.cli.smallbaselineApp import main as smallbaselineApp


class InSARProcessor:
    """Processing object for the InSAR data

    This class contains the code needed to download and process new
    InSAR data

    Attributes
    ----------
    succesfull : list
        After running, will contain a list of volcano/asf_name
        combinations for which the MintPy run completed normally.
    failed : list
        After running, will contain a list of volcano/asf_name
        combinations for which processing failed for any reason, along
        with a string stating the reason for failure.

    Methods
    -------
    run()
        Shortcut function to run all processing steps other than upload
    update_projects()
        Update ASF projects, and mark associated volcanoes for update
    process_volcanoes()
        Run processing for any volcanoes marked for update
    ensure_downloads(volcano,proj_downloads)
        Download ASF files for asf_project, if not already downloaded
    grab_ifg(path, frame, proj_downloads)
        copy interferograms for the selected path/frame to the products
        directory
    run_mintpy(volcano, proj_downloads)
        Run the MintPy processor on the given volcano to produce
        timeseries and velocity files
    upload_files()
        Transfer the files from the products directory to the server
    """

    def __init__(
            self,
            debug: bool = False,
            custom_asf: list | None = None,
            custom_volc: list | None = None,
            force: bool = False):
        """
        Parameters
        ----------
        debug : bool
            Flag indicating if we should use the debug/testing hyp3 or
            the full production hyp3
        custom_asf : list, optional
            If provided, a list of ASFArea objects as defined in
            config.py to be considered for processing. Overrides the
            default config.asf_list (default: None)
        custom_volc : list, optional
            If provided, a list of VolcanoArea objects as defined in
            config.py to be considered for processing. Overrides the
            default config.volcano_list (default: None)
        force : bool, optional
            Force generation of product for all volcanoes associated
            with selected ASF projects, regardless of if the project is
            updated or not (default: False)
        """

        # List of succesfull and failed volcanoes/paths.
        # Populated after calling run_mintpy
        self.successful = []
        self.failed = []

        if not debug:
            self._hyp3 = sdk.HyP3(
                'https://hyp3-avo.asf.alaska.edu',
                prompt=True,
                username='ycheng',
                password='earthdata+1S'
            )
        else:
            self._hyp3 = sdk.HyP3(prompt=True, username='ycheng', password='earthdata+1S')

        # The ASF projects to be updated
        self._asf_projects = custom_asf or config.asf_list

        # The volcanoes to generate files for (if their ASF project has updates)
        self._volcanoes = custom_volc or config.volcano_list

        # Top level directory to store the processing directories in
        self._processing_dir = Path(__file__).parent / 'processings'

        # Directory to store the output InSAR products in
        self._product_dir = Path(os.path.dirname(__file__), 'products')

        # Use a temporary directory to store the downloaded files, so we
        # only have to download once per asf_name. The downloaded files
        # will be copied into the processing directory when needed.
        # This directory will be automatically removed when class is destroyed.
        self._download_dir = tempfile.TemporaryDirectory()
        self._downloads = Path(self._download_dir.name)

        self._debug = debug
        self._force = force

    def run(self) -> (list, list):
        """Run all processing steps, excluding file transfer to server

        Returns
        -------
        successful : list
            List of volcanoes and associated ASF project names for which
            generation ran succesfully
        failed : list
            List of volcanoes, associated ASF project names, and reason
            messages for which generation failed.
        """

        self.update_projects()
        return self.process_volcanoes()

    def update_projects(self):
        """ Update the projects at ASF, and mark any volcanoes
        associated with updated projects.

        Should the ASF search function return an error, any volcanoes
        associated with that project will be added to the failed list,
        and no generation will be attempted for those volcanoes.
        """

        # The last ASF project submitted for update, if any.
        watch_name = None

        for asf_project in self._asf_projects:
            # Note: if something dies after running this, but before
            # processing, this returns an up-to-date flag on the next
            # run, potentially resulting in files not getting updated
            # for one or more volcanoes/paths/frames.
            asf_flag = avo_insar_functions.update_asf_project(
                asf_project.path,
                asf_project.frame,
                asf_project.asf_name,
                self._hyp3
            )  # this function checks updates AND submit requests to ASF

            # If the force flag is set, mark all volcanoes for
            # generation, unless the ASF project check failed.
            if self._force and asf_flag == 0:
                asf_flag = 1

            if asf_flag > 0:
                # We requested an update of a project, so mark that we
                # need to watch for it to finish. At the end of the loop,
                # this variable will contain the last project submitted,
                # which presumably will be the last to complete.
                watch_name = asf_project.asf_name

                # Volcano update flag defaults to zero, so set it if
                # asf_flag is 1
                for volc in config.volc_lookup[asf_project.asf_name]:
                    volc.update_flag(asf_flag)

            elif asf_flag == -1:
                # Mark volcanoes associated with this project as "failed",
                # since we were unable to check or update the associated
                # ASF project.
                for volc in config.volc_lookup[asf_project.asf_name]:
                    self.failed.append(
                        f"{volc.volc_name} - {volc.asf_name}: Unable to check/update ASF project"
                    )

        if watch_name is not None:
            # wait for the last project submitted to complete.
            # May take several hours.
            jobs = self._hyp3.find_jobs(name=watch_name)
            jobs = self._hyp3.watch(jobs)

    def process_volcanoes(self) -> (list, list):
        """ Call required processing functions on all volcanoes in a
        parallel processing manor.

        Includes downloading projects from ASF, capturing interferograms,
        and running MintPy

        Populates the successful and failed attributes.

        Returns
        -------
        successful : list
            List of volcanoes and associated ASF project names for which
            generation ran succesfully
        failed : list
            List of volcanoes, associated ASF project names, and reason
            messages for which generation failed.
        """

        # Clean and re-create the output directory before starting the run.
        shutil.rmtree(str(self._product_dir), ignore_errors=True)
        self._product_dir.mkdir(parents=True, exist_ok=True)

        # Directory to hold insar timeseries/velocity files
        insar_dir = self._product_dir / 'insar'
        insar_dir.mkdir(exist_ok=True)

        # Directory to hold interferogram kml files
        insar_dir = self._product_dir / 'kml'
        insar_dir.mkdir(exist_ok=True)

        # MintPy processes list
        processings = []

        # Run volcanoes in parallel
        with ProcessPoolExecutor() as executor:
            for volcano in self._volcanoes:
                if volcano.run_flag != 1:
                    continue

                # The directory holding the downloaded files for this
                # volcano's path/frame
                proj_downloads: Path = self._downloads / volcano.asf_name

                # Make sure all files have been downloaded for this
                # path/frame combination
                self.ensure_downloads(volcano, proj_downloads)

                # The following commented lines are if *NOT* running in
                # parallel, the rest of the function is for when
                # parallel processing is desired
                # Pick one or the other, not both :)
                # ------- Single processing ---------------#
                # success, result = self.run_mintpy(volcano, proj_downloads)
                # if success:
                #     self.successful.append(result)
                # else:
                #     self.failed.append(result)
                # ---------End Single Processing-------------#

            # ---------Parallel Processing --------------#
                # Submit the mintpy run to be processed in a parallel
                # fashion
                future = executor.submit(self.run_mintpy, volcano, proj_downloads)
                processings.append(future)

            # Once MintPy runs for all volcanoes are submitted, loop
            # through the results as they become available
            for future in processings:
                success, result = future.result()
                if success:
                    self.successful.append(result)
                else:
                    self.failed.append(result)
            # ------------End Parallel Processing ----------#

        return (self.successful, self.failed)

    def ensure_downloads(self, volcano: config.VolcanoArea, proj_downloads: Path) -> None:
        """Check for existing downloads for the ASF project associated
        with this volcano, and download if needed.

        Will also copy interferogram files from the download to the
        products directory when downloading.

        Parameters
        ----------
        volcano : VolcanoArea
            The volcano to ensure we have downloaded files for
        proj_downloads:
            The path where the downloaded files should be stored.
        """
        if not proj_downloads.exists():
            print(f"Downloading files for {volcano.asf_name}")
            avo_insar_functions.avo_insar_download(
                self._hyp3,
                volcano.asf_name,
                proj_downloads
            )

            # Grab any interferograms from this download
            self.grab_ifg(volcano.path, volcano.frame, proj_downloads)
        else:
            print(f"Files for {volcano.asf_name} already downloaded. Skipping download.")

    def grab_ifg(self, path: int, frame: int, proj_downloads: Path) -> None:
        """Copy interferogram kml files to the products directory

        Parameters
        ----------
        path : int
            The path to copy interferograms for
        frame : int
            The frame to copy interferograms for
        proj_downloads : Path
            The directory containing the downloaded files
        """

        # Compile the path to the directory into which the
        # interferograms should be copied.
        # The directory is based on the path, frame, and date range of
        # the interferogram.
        path_frame = f"path{path}frame{frame}"
        kml_dir = self._product_dir / 'kml' / path_frame

        for f in proj_downloads.glob('S1*/*color_phase.kmz'):
            # Extract the start and end date from the filename
            file_date = f.name[5:13] + '_' + f.name[21:29]
            date_dir: Path = kml_dir / file_date
            date_dir.mkdir(parents=True, exist_ok=True)

            shutil.copy(f, date_dir)

    def run_mintpy(self, volcano: config.VolcanoArea, proj_downloads: Path) -> (bool, str):
        """Run MintPy processing on the specified volcano

        Creates the velocity.h5 and timeseries.h5 files for the volcano,
        and places them in the products directory.

        Parameters
        ----------
        volcano : VolcanoArea
            The volcano to process
        proj_downloads : Path
            The directory containing the downloaded ASF project files
            for this volcano.

        Returns
        -------
        success : bool
            A flag indicating if this was a successful run or not
        result_string : str
            A string indicating the volcano, ASF project name, and
            additional information, if any, about the result of the run.
        """

        # Make sure we're in a good directory so MintPy doesn't fail (seriously???)
        os.chdir(os.path.dirname(__file__))

        print('########CURRENT PROJECT########')
        project_name = volcano.volc_name + str(volcano.path)
        analysis_directory: Path = self._processing_dir / project_name
        mintpy_directory = analysis_directory / 'MintPy'

        print(f"analysis_directory: {analysis_directory}")

        # Initalize to default of success. We're optimistic here!
        success = True
        result_string = f"{volcano.volc_name} - {volcano.asf_name}"

        # Remove any existing processing directories. Leaving them can cause issues with leftover
        # files from previous runs.
        shutil.rmtree(analysis_directory, ignore_errors=True)

        # Copy the download files into the analysis_directory
        # Much faster than downloading again if we already have them.
        # Don't copy over any files that are filtered for this volcano.
        filter_dates = volcano.filter_dates
        for f in proj_downloads.glob('*'):
            if str(f.name) not in filter_dates:
                shutil.copytree(f, analysis_directory / f.name, dirs_exist_ok=True)

        # .tif files to be merged into the full area image
        merge_paths = list(analysis_directory.glob('*/*_amp.tif'))

        if not merge_paths:
            print(f"No images found for {volcano.volc_name}")
            return  # No data for this volcano

        full_scene = analysis_directory / "full_scene.tif"  # create a full scene for cropping

        # gdal_merge expects a sys.argv argument list in which the first
        # argument is always the name of the script.
        # Arguments: -o <output_file> input_file1 ... input_fileN
        merge_args = ['gdal_merge.py', '-o', str(full_scene)] + [str(x) for x in merge_paths]
        gdal_merge(merge_args)

        # Create the vrt image
        image_file = f"{analysis_directory}/raster_stack.vrt"
        vrt_options = gdal.BuildVRTOptions(separate=True)
        gdal.BuildVRT(image_file, [str(full_scene), ], options=vrt_options)

        # Crop the image to the volcano area
        avo_insar_functions.avo_insar_crop(
            image_file,
            volcano.ul,
            volcano.lr,
            analysis_directory
        )

        # Create a config file for MintPy and return the path to said file
        mintpy_config = avo_insar_functions.avo_insar_run(analysis_directory, mintpy_directory)

        # Run MintPy, keeping track of success and failure
        app_args = ['--dir', str(mintpy_directory), str(mintpy_config)]
        try:
            smallbaselineApp(app_args)
        except Exception as e:
            # If we get some sort of exception running mintpy, capture
            # the exception string along with the volcano and ASF
            # project names.
            success = False
            result_string = f"{volcano.volc_name} - {volcano.asf_name}: {e}"
        else:
            # Yay, it worked!
            # Move the products to the output directory
            canonical_name = volcano.volc_name.lower().replace(' ', '')
            output_ident = f"{canonical_name}_main_path{volcano.path}.h5"
            for product in ('timeseries_ERA5_demErr', 'velocity'):
                dest = product.split('_')[0]  # timeseries or velocity
                shutil.move(
                    str(mintpy_directory / f"{product}.h5"),
                    str(self._product_dir / 'insar' / f"{dest}_{output_ident}")
                )

        # remove the processing directory, since we are now done with it
        shutil.rmtree(str(analysis_directory), ignore_errors=True)

        return (success, result_string)

    def upload_files(self):
        """Upload the product files to the server

        This uses command-line rsync to push files using a key file for
        authentication. This key must be obtained seperately,
        and the function parameters changed appropriately if a different
        destination is desired.
        """

        # -------- Destination server properties -------- #
        # --- Change as needed for desired destination ---#
        # dst format: user@server.name:/path/on/dest/server
        dst = 'geodesy@apps.avo.alaska.edu:/geodesy/data/'
        if self._debug:
            dst += 'test/'

        dst_port = 2200
        key_file = os.path.join(os.path.dirname(__file__), 'id_rsa')
        ###############################################

        src = str(self._product_dir) + "/"

        cmd = [
            'rsync',
            '-r',   # Do a recursive copy (directories)
            '--stats',  # Show a summary when complete
            '-e', f'ssh -i {key_file} -p {dst_port}',  # Use SSH with key and port
            src,
            dst
        ]

        # run the command using the subprocess module
        result = subprocess.run(cmd)

        # Print any output returned
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
    for s in processor.successful:
        print(" - ", s)
    print("#################################################")
    print(f"Run complete at {datetime.now().strftime('%m/%d/%y %H:%M')}")
