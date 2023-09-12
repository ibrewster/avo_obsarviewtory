## import packages
import numpy as np
import asf_notebook as asfn

from osgeo import gdal
import shutil
from pathlib import Path

import pandas as pd
from dateutil.parser import parse as parse_date
from datetime import timedelta
import asf_search as asf

import hyp3_sdk as sdk


def avo_insar_download( hyp3, asf_name , analysis_directory , filter_dates ):
# download project {asf_name} into {analysis_directory}
    jobs = hyp3.find_jobs(name=asf_name)
    print(f"\nProject: {jobs.jobs[0].name}")
    project_zips = jobs.download_files(analysis_directory) # download
    for z in project_zips:
        asfn.asf_unzip(str(analysis_directory), str(z)) # unzip
        z.unlink()

#     ifg download has become an function itself
#     color_files = analysis_directory.glob(f"S1*/*2023*color_phase.kmz")
#     color_files_list = list(color_files)
#     color_dir = analysis_directory/"colorphase"
#     color_dir.mkdir(exist_ok=True)
#     for file in color_files_list:
#         file.rename(color_dir / file.name) # move color phase interferograms

    if len(filter_dates) > 0: # remove bad dates
        for filter_date in filter_dates:
            remove_date = analysis_directory / filter_date
            shutil.rmtree(remove_date)

    for pattern in ["xml","png","kmz","md.txt"]:
        unneeded_files = analysis_directory.glob(f"S1*/*.{pattern}") # remove files not needed for processing
        for file in unneeded_files:
            file.unlink()

    amp = list(analysis_directory.glob(f'*/*_amp.tif'))
    merge_paths = ""

    for pth in amp:
        merge_paths = f"{merge_paths} {pth}"

    full_scene = analysis_directory/"full_scene.tif" # create a full scene for cropping
    if full_scene.exists():
        full_scene.unlink()
    gdal_command = f"gdal_merge.py -o {full_scene} {merge_paths}"

    return(gdal_command) # I have to return this and run it in the notebook because I cannot run bash commands inside a function definition


def avo_insar_crop( image_file , ul , lr , analysis_directory ):
# crop downloaded files; these two functions are seperated because I have to run a bash command between them
    img = gdal.Open(image_file)
    rasterstack = img.ReadAsArray()

    fnames = list(analysis_directory.glob('*/*.tif'))
    fnames.sort()

    for i, fname in enumerate(fnames):
        clip = fname.parent/f"{fname.stem}_clip.tif"
        gdal.Translate(destName=str(clip), srcDS=str(fname), projWin=[ul[0], ul[1], lr[0], lr[1]])
        gdal.Warp(str(clip), str(clip), dstSRS='EPSG:4326', dstNodata=0)
        fname.unlink()

    fnames = list(analysis_directory.glob('*/*.tif*'))
    fnames = [str(f) for f in fnames]
    fnames.sort()

    removed = []
    for f in fnames:
        if not "dem" in str(f):
            raster = gdal.Open(f)
            if raster:
                band = raster.ReadAsArray()
                if np.count_nonzero(band) < 1:
                    Path(f).unlink()
                    removed.append(f)
    if len(removed) == 0:
        print("No Geotiffs were removed")
    else:
        print(f"{len(removed)} GeoTiffs removed:")
        for f in removed:
            print(f)


def avo_insar_run( analysis_directory , mintpy_directory ): # preparation for running MintPy
    if not mintpy_directory.is_dir():
        mintpy_directory.mkdir()
    mintpy_config = mintpy_directory / 'mintpy_config.txt'
    mintpy_config.write_text(
f"""
mintpy.load.processor        = hyp3
##---------interferogram datasets:
mintpy.load.unwFile          = {analysis_directory}/*/*_unw_phase_clip.tif
mintpy.load.corFile          = {analysis_directory}/*/*_corr_clip.tif
##---------geometry datasets:
mintpy.load.demFile          = {analysis_directory}/*/*_dem_clip.tif
mintpy.load.incAngleFile     = {analysis_directory}/*/*_lv_theta_clip.tif
mintpy.load.azAngleFile      = {analysis_directory}/*/*_lv_phi_clip.tif
mintpy.load.waterMaskFile    = {analysis_directory}/*/*_water_mask_clip.tif
""")
    return mintpy_config


def check_project_update( asf_name , record_dates ):
# check if project {asf_name} can be updated
# note that path30 / frame420 and path81 / frame166 always fail; maybe because of their longitude ranges
    for record in record_dates:
        if record.asf_name == asf_name:
            last_date = parse_date(record.last_date).date()
            search_results = asf.search(
                platform=asf.SENTINEL1,
                frame=record.frame,
                relativeOrbit=record.path,
                processingLevel='SLC'
            )

            if len(search_results)>1:
                baseline_results = search_results[-1].stack()
                if len(baseline_results)==0:
                    print('An ASF search problem has occurred. Check failed at project '+asf_name+'.')
                    return(-1)

                columns = list(baseline_results[0].properties.keys()) + ['geometry', ] # these 4 lines are to extract search result
                data = [list(scene.properties.values()) + [scene.geometry, ] for scene in baseline_results]
                stack = pd.DataFrame(data, columns=columns)
                stack['startTime'] = stack.startTime.apply(parse_date)

                new_date = stack.startTime.iloc[-1].date()
                delta_date = new_date-last_date

                if delta_date.days>1:
                    print('    The project '+asf_name+' can be updated. New SLC is on '+str(new_date)+' ('+str(delta_date.days)+' days later).')
                    return(1)
                else: # when delta_date.days<=0
                    print('    The project '+asf_name+' is up to date.')
                    return(0)
            else: # when len(search_results)==0
                print('An ASF search problem has occurred. Check failed at project '+asf_name+'.')
                return(-1)


def update_asf_project( path, frame, asf_name, hyp3):
# update the given project {asf_name}
    jobs = hyp3.find_jobs(name=asf_name)

    # TODO: how to handle no jobs - some random min date?
    last_date = max( asfn.get_job_dates(jobs) )
    last_date = parse_date(last_date).date()

    #TODO: can we limit this by date? 30 second timeout means timeouts are frequent.
    search_results = asf.search(
        platform=asf.SENTINEL1,
        frame=frame,
        relativeOrbit=path,
        processingLevel='SLC',
        start = '1 month ago'
    )

    if len(search_results)>1:
        #TODO: Handle errors with stack (ValueError No products found matching stack parameters, requests.exceptions.JSONDecodeError, etc)
        baseline_results = search_results[-1].stack()
        if len(baseline_results)==0:
            print('An ASF search problem has occurred. Check failed at project '+asf_name+'.')
            return( -1 )

        columns = list(baseline_results[0].properties.keys()) + ['geometry', ] # these lines extract search result
        data = [list(scene.properties.values()) + [scene.geometry, ] for scene in baseline_results]
        stack = pd.DataFrame(data, columns=columns)
        stack['startTime'] = stack.startTime.apply(parse_date)

        new_date = stack.startTime.iloc[-1].date()
        delta_date = new_date-last_date

        if delta_date.days>4:
            sbas_pairs = set()
            newstack = stack.loc[( pd.Timestamp(last_date+timedelta(days=-2),tz='UTC') <= stack.startTime) & (stack.startTime <= pd.Timestamp(new_date+timedelta(days=2),tz='UTC') )]
            for reference, rt in newstack.loc[::-1, ['sceneName', 'temporalBaseline']].itertuples(index=False):
                secondaries = newstack.loc[
                    (newstack.sceneName != reference)
                    & (newstack.temporalBaseline - rt <= 48) # 48 for max temporal baseline
                    & (newstack.temporalBaseline - rt > 0)
                ]
                for secondary in secondaries.sceneName:
                    sbas_pairs.add((reference, secondary))

            last_year_time  = pd.Timestamp(new_date + timedelta(days=-365), tz='UTC')
            last_year_scene = stack.iloc[(stack['startTime'] - last_year_time).abs().idxmin()]
            new_time = pd.Timestamp(new_date, tz='UTC')
            new_scene = stack.iloc[(stack['startTime'] - new_time).abs().idxmin()]
            sbas_pairs.add((last_year_scene['sceneName'], new_scene['sceneName']))

            sbas_pairs_list = list()
            for tuple_name in sbas_pairs:
                sbas_pairs_list.append(list(tuple_name))

            jobs = sdk.Batch()
            for reference, secondary in sbas_pairs_list:
                jobs += hyp3.submit_insar_job(reference, secondary, name=asf_name,
                                              include_dem=True, include_look_vectors=True,
                                              include_inc_map=True, include_displacement_maps=True,
                                              apply_water_mask=True)
            print(f"Updated ASF project submitted for {asf_name}. Your new subset contains {len(sbas_pairs)} more pairs:")
            for line in sbas_pairs_list:
                print('        '+line[0][17:25]+'_'+line[1][17:25])
            return( 1 )
        else:
            print('    The project '+asf_name+' is up to date.')
            return( 0 )
    else: # when len(search_results)==0
        print('An ASF search problem has occurred. Check failed at project '+asf_name+'.')
        return( -1 )

def avo_insar_difg( hyp3, asf_name , analysis_directory , date_range ):
# download interferograms within {date_range} from project {asf_name} into {analysis_directory}
    jobs = hyp3.find_jobs(name=asf_name)
    print(f"\nProject: {jobs.jobs[0].name}")
    jobs = asfn.filter_jobs_by_date(jobs, date_range)
    project_zips = jobs.download_files(analysis_directory) # download
    for z in project_zips:
        asfn.asf_unzip(str(analysis_directory), str(z)) # unzip
        z.unlink()

    color_files = analysis_directory.glob(f"S1*/*2023*color_phase.kmz")
    color_files_list = list(color_files)
    color_dir = analysis_directory/"colorphase"
    color_dir.mkdir(exist_ok=True)
    for file in color_files_list:
        file.rename(color_dir / file.name) # move color phase interferograms

    ifg_number = len(color_files_list)

    return(ifg_number)
