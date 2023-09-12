# avo_obsarviewtory


This [Alaska Volcano Observatory](https://avo.alaska.edu/) (AVO) repository contains an integrated tool for analyzing [Sentinel-1](https://sentinel.esa.int/web/sentinel/missions/sentinel-1) Interferometric Synthetic Aperture Radar (InSAR) data of Alaska volcanoes. 

This tool uses the [Alaska Satellite Facility](https://asf.alaska.edu/)’s [Hybrid Pluggable Processing Pipeline](https://github.com/ASFHyP3/hyp3) (ASF HyP3) to search and download SAR data, and runs a small baseline subset analysis with [MintPy software](https://github.com/insarlab/MintPy). Such analysis contains the following steps:

<ol start="0">
  <li> ASF analyzes and releases a new single look complex (SLC) data file</li>
</ol>
Then this tool can be run to do the following:


1. Create inteferograms for the new SLC and add them to their corresponding ASF project list
2. Wait for ASF to process the new inteferograms
3. Download processed inteferograms, crop them into the area-of-interest, and clean up those with low coherence or shifting frames
4. Run MintPy processing for the prepared inteferograms

 
## Notebooks
This tool contains 7 Notebooks for now:
1.  [`avoobs_init.ipynb`](https://github.com/uafgeotools/avo_obsarviewtory/blob/main/avoobs_init.ipynb): This Notebook initializes the project by setting up the neccessary directory structures and parameters. It does the latter by saving parameters into data files that the other Notebooks can read. Running this Notebook will reset your data files.
2. [`avoobs_routine_processing.ipynb`](https://github.com/uafgeotools/avo_obsarviewtory/blob/main/avoobs_main_processing.ipynb): This Notebook runs processing for all preset volcanoes. By design, this Notebook will be run weekly to keep generating the latest products. After running (which often takes days), we're now using [`avoobs_transfer.ipynb`](https://github.com/uafgeotools/avo_obsarviewtory/blob/main/avoobs_transfer.ipynb) to move the products files for easier transfering.
3. [`avoobs_ifg_download.ipynb`](https://github.com/uafgeotools/avo_obsarviewtory/blob/main/avoobs_ifg_download.ipynb): This Notebook downloads interferograms from a given time range. This function was in `routine_processing` Notebook and is now seperated.
4. [`avoobs_transfer.ipynb`](https://github.com/uafgeotools/avo_obsarviewtory/blob/main/avoobs_transfer.ipynb): This Notebook helps transfer product files after a routine processing or a ifg downnload is done.
5. [`avoobs_update_check.ipynb`](https://github.com/uafgeotools/avo_obsarviewtory/blob/main/avoobs_update_check.ipynb): This Notebook checks if there are any new SLCs released by ASF. Known bug: [`asf_search`](https://github.com/asfadmin/Discovery-asf_search) ALWAYS fails for Sentinel-1 path-30-frame-420 and path-81-frame-166, and it sometimes fails for other paths.
6. [`avoobs_select_processing.ipynb`](https://github.com/uafgeotools/avo_obsarviewtory/blob/main/avoobs_select_processing.ipynb): This Notebook allows the user to select a specific volcano (or specific volcanoes) and run a processing that has the described 4 steps.
7. [`MintPy_Time_Series_Copy1.ipynb`](https://github.com/uafgeotools/avo_obsarviewtory/blob/main/MintPy_Time_Series_Copy1.ipynb): This Notebook runs a timeseries analysis for a given project with more detailed parameter settings. Usually when the routine processing fails, we can try this.

And there is a `test.ipynb` that includes some simple functions.


## Dependencies:
This project requires dependencies to comply, and all needed packages should be found from file [`insar_new.yml`](https://github.com/uafgeotools/avo_obsarviewtory/blob/main/insar_new.yml).

Besides packages, another prerequisite is a completed local account configuration for Copernicus Climate Change Service. A tutorial on this could be found [here](https://github.com/Alex-Lewandowski/opensarlab-notebooks/blob/master/SAR_Training/English/Master/MintPy_Time_Series_From_Prepared_Data_Stack.ipynb), in the section "1. Add Your Climate Data Store (CDS) UID & API Key to the Pyaps3 Config", by [Alex-Lewandowski](https://github.com/Alex-Lewandowski).


## Output
*to be added*

## Examples
*to be added*

## Contribution
[rgrapenthin](https://github.com/rgrapenthin) is the director of this repository and envisioned most of the functionality of the project.

The Notebook ["2018 Kīlauea volcano analysis with HyP3 AVO and MintPy"](https://gist.github.com/jhkennedy/e9e7ec353b2a05419e50413368ff0505) by [jhkennedy](https://github.com/jhkennedy) provides improtant and the very original reference for this tool.

## References
Yunjun, Z., Fattahi, H., and Amelung, F. (2019), Small baseline InSAR time series analysis: Unwrapping error correction and noise reduction, _Computers & Geosciences_, _133_, 104331, doi:[10.1016/j.cageo.2019.104331](https://doi.org/10.1016/j.cageo.2019.104331), [arXiv](https://eartharxiv.org/9sz6m/), [data](https://zenodo.org/record/4743058), [notebooks](https://github.com/geodesymiami/Yunjun_et_al-2019-MintPy).
