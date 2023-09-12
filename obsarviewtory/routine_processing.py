try:
    # Module
    from . import config, avo_insar_functions
except ImportError:
    # Script
    import config, avo_insar_functions


import hyp3_sdk as sdk
from pathlib import Path


if __name__ == "__main__":
    flags = [] # this variable records if a project should be updated
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

        flags.append( asf_flag ) # save the status: can be updated?

        # TODO: Isn't the flag just a 1 or a 0?
        asf_project.update_date(asf_flag)


    watch_name = 'name' # this variable records an asf_name
    # TODO: make this a dictionary lookup
    for i in range(len(flags)):
        # There is one flag per item in the asf_list, so the first loop here
        # associates the flag with the index of the item in the asf_list
        for volcano in config.volcano_list:
            # Go through the list of volcanoes, and find the one(s) where the asf_name
            # item in the volcano item matches this asf item, so we can update the
            # flag on that item.
            if volcano.asf_name == config.asf_list[i].asf_name:
                volcano.update_flag( flags[i] )
        if flags[i] == 1:
            watch_name = config.asf_list[i].asf_name # always save the lastly-submitted project for watch

    # TODO: Watch name defaults to 'name', so it will NEVER be "0". Ask about the logic here.
    if watch_name != 0:
        jobs = hyp3.find_jobs(name=watch_name)
        jobs = hyp3.watch(jobs) # wait until asf has processed all submitted requests


    for volcano in config.volcano_list:
        if volcano.run_flag == 1: # run all processings that can be updated

            print('########CURRENT PROJECT########')
            project_name = volcano.volc_name + str(volcano.path)
            analysis_directory = Path.cwd() / 'processings' / project_name
            mintpy_directory = analysis_directory / 'MintPy'
            print(f"analysis_directory: {analysis_directory}")

            gdal_command = avo_insar_functions.avo_insar_download( hyp3 , volcano.asf_name , analysis_directory , volcano.filter_dates)
            full_scene = analysis_directory/"full_scene.tif"
            if full_scene.exists():
                full_scene.unlink()

            #!{gdal_command}
            image_file = f"{analysis_directory}/raster_stack.vrt"
            #!gdalbuildvrt -separate $image_file -overwrite $full_scene

            avo_insar_functions.avo_insar_crop(image_file, volcano.ul, volcano.lr, analysis_directory)

            mintpy_config = avo_insar_functions.avo_insar_run( analysis_directory , mintpy_directory )
            #!smallbaselineApp.py --dir {mintpy_directory} {mintpy_config}
            clean_command = f"rm -rf {analysis_directory}/S1*"
            #!clean_command
