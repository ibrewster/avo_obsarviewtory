import os
import shutil
import tempfile

from osgeo import gdal

try:
    # Module
    from . import config, avo_insar_functions, gdal_merge
except ImportError:
    # Script
    import config, avo_insar_functions, gdal_merge


import hyp3_sdk as sdk
from pathlib import Path
from mintpy.cli.smallbaselineApp import main as smallbaselineApp


if __name__ == "__main__":
    watch_name = None

    #hyp3 = sdk.HyP3('https://hyp3-avo.asf.alaska.edu', prompt=True, username='ycheng', password='earthdata+1S')
    hyp3 = sdk.HyP3(prompt=True, username='ycheng', password='earthdata+1S')

    for asf_project in config.asf_list:
        # TODO: if something dies before processing, this returns an up-to-date flag
        asf_flag = avo_insar_functions.update_asf_project(
            asf_project.path,
            asf_project.frame,
            asf_project.asf_name,
            hyp3
        ) # this function checks updates AND submit requests to ASF

        ##########DEBUG##########
        asf_flag = 1
        #########################

        if asf_flag:
            # We requested an update of something, so mark that we need to watch for it to finish.
            watch_name = asf_project.asf_name
        else:
            # We only need to run this if the flag is 0, since the flag defaults to 1
            for volc in config.volc_lookup[asf_project.asf_name]:
                volc.update_flag(asf_flag)

        # TODO: Isn't the flag just a 1 or a 0?
        asf_project.update_date(asf_flag)


    if watch_name is not None:
        jobs = hyp3.find_jobs(name=watch_name)
        jobs = hyp3.watch(jobs) # wait until asf has processed all submitted requests. May be several hours.


    names_downloaded = []

    #cwd gets changed while running the loop, so declare this outside the loop.

    processed_file_path = Path.cwd() / 'processings'
    with tempfile.TemporaryDirectory() as download_dir:
        download_dir = Path(download_dir)

        for volcano in config.volcano_list:
            if volcano.run_flag != 1:
                continue


            print('########CURRENT PROJECT########')
            project_name = volcano.volc_name + str(volcano.path)
            proj_downloads = download_dir / volcano.asf_name

            analysis_directory: Path =  processed_file_path / project_name
            mintpy_directory = analysis_directory / 'MintPy'

            print(f"analysis_directory: {analysis_directory}")

            if volcano.asf_name not in names_downloaded:
                avo_insar_functions.avo_insar_download(
                    hyp3,
                    volcano.asf_name,
                    proj_downloads,
                    volcano.filter_dates
                )

                names_downloaded.append(volcano.asf_name)


            # Remove any existing output directories
            shutil.rmtree(analysis_directory, ignore_errors = True)

            # Make sure the output directories exist
            # os.makedirs(mintpy_directory, exist_ok = True)

            # Copy the download files into the analysis_directory
            # Much faster than downloading again if we already have them downloaded.
            for f in proj_downloads.glob('*'):
                shutil.copytree(f, analysis_directory/f.name, dirs_exist_ok = True)

            merge_paths = list(analysis_directory.glob(f'*/*_amp.tif'))

            if not merge_paths:
                print(f"No images found for {volcano.volc_name}")
                continue # No data for this volcano

            full_scene = analysis_directory/"full_scene.tif" # create a full scene for cropping
            if full_scene.exists():
                full_scene.unlink()

            merge_args = ['gdal_merge.py','-o', str(full_scene)] + [str(x) for x in merge_paths]
            gdal_merge.main(merge_args)
            image_file = f"{analysis_directory}/raster_stack.vrt"
            if os.path.exists(image_file):
                os.unlink(image_file)

            vrt_options = gdal.BuildVRTOptions(separate = True)
            gdal.BuildVRT(image_file, [str(full_scene), ], options = vrt_options)
            #!gdalbuildvrt -separate $image_file -overwrite $full_scene

            avo_insar_functions.avo_insar_crop(image_file, volcano.ul, volcano.lr, analysis_directory)

            mintpy_config = avo_insar_functions.avo_insar_run( analysis_directory , mintpy_directory )
            app_args = ['--dir', str(mintpy_directory), str(mintpy_config)]

            try:
                smallbaselineApp(app_args)
            except Exception as e:
                print(f"Unable to produce output for {volcano.volc_name}: {str(e)}")
            else:
                print("!!!!!GOT ONE!!!!!")

            for d in analysis_directory.glob("S1*"):
                shutil.rmtree(str(d), ignore_errors = True)
