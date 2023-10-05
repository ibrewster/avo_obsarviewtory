import os
import re
import zipfile  # for extractall, ZipFile, BadZipFile

from datetime import date
from typing import List

from hyp3_sdk import Batch

#######################
#  Utility Functions  #
#######################

def path_exists(path: str) -> bool:
    """
    Takes a string path, returns true if exists or
    prints error message and returns false if it doesn't.
    """
    assert type(path) == str, 'Error: path must be a string'

    if os.path.exists(path):
        return True
    else:
        print(f"Invalid Path: {path}")
        return False
    
def asf_unzip(output_dir: str, file_path: str):
    """
    Takes an output directory path and a file path to a zipped archive.
    If file is a valid zip, it extracts all to the output directory.
    """
    ext = os.path.splitext(file_path)[1]
    assert type(output_dir) == str, 'Error: output_dir must be a string'
    assert type(file_path) == str, 'Error: file_path must be a string'
    assert ext == '.zip', 'Error: file_path must be the path of a zip'

    if path_exists(output_dir):
        if path_exists(file_path):
            print(f"Extracting: {file_path}")
            try:
                zipfile.ZipFile(file_path).extractall(output_dir)
            except zipfile.BadZipFile:
                print(f"Zipfile Error.")
            return
        
#######################################
#   Product Related Utility Functions #
#######################################
def date_from_product_name(product_name: str) -> str:
    regex = "\w[0-9]{7}T[0-9]{6}"
    results = re.search(regex, product_name)
    if results:
        return results.group(0)
    else:
        return None
    
    
#########################
#  Hyp3v2 API Functions #
#########################
def get_job_dates(jobs: List[str]) -> List[str]:
    dates = set()
    for job in jobs:
        for granule in job.job_parameters['granules']:
            dates.add(date_from_product_name(granule).split('T')[0])
    return list(dates)

def filter_jobs_by_date(jobs, date_range):
    remaining_jobs = Batch()
    for job in jobs:
        for granule in job.job_parameters['granules']:
            dt = date_from_product_name(granule).split('T')[0]
            aquistion_date = date(int(dt[:4]), int(dt[4:6]), int(dt[-2:]))
            if date_range[0] <= aquistion_date <= date_range[1]:
                remaining_jobs += job
                break
    return remaining_jobs