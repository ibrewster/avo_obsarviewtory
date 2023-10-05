"""Run the AVO obSARViewtory processing code

Generates timeseries and velocity .h5 files and copies interferograms
from ASF projects, and uploads them to the server.
"""

import time
from datetime import datetime

from obsarviewtory import InSARProcessor, config

if __name__ == "__main__":
    # record the start time so we can calculate total run time easily.
    t_start = time.time()
    print(f"Run starts at {datetime.now().strftime('%m/%d/%y %H:%M')}")

    # Custom ASF scene list to process
    asf_list = [
        config.path44_410,
        config.path50_182,
        config.path81_166
    ]    

    processor = InSARProcessor(debug = True, custom_asf = asf_list, force = True)
    successful, failed = processor.run()
    # processor.upload_files()

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
    for f in failed:
        print(" - ", f)

    print('-------------------')
    print("Succesfully generated files for:")
    for s in successful:
        print(" - ", s)
    print("#################################################")
    print(f"Run complete at {datetime.now().strftime('%m/%d/%y %H:%M')}")    