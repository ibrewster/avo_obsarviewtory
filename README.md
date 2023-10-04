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


## Dependencies:
- Python 3.10 or later is required due to the type annotations used in the routine_processing.py file. If an earlier version of python is required, modifications to the type annotations will be needed.
- correct installation of the pykdtree library requires the OpenMP libraries to be installed at the system level.

Most dependencies can be found in the requirements.txt file, and installed via the following commands:

```sh
export USE_OMP="probe"
pip install numpy
pip install --no-cache-dir --no-binary pykdtree -r requirements.txt
```

*** note
[!IMPORTANT]
numpy *does* need to be installed seperately _first_, otherwise gdal will not build/install correctly. The `--no-cache-dir` flag is used to make sure the version of gdal installed isn't a cached version _without_ numpy support, and the `--no-binary pykdtree` flag ensures that pykdtree is built with OpenMP support. Depending on your enviroment, these two flags may not be needed.
***

*** note
If installing on an Apple Silicon machine, pygrib may need to be built from source as well, using the following command:
```
ECCODES_DIR=/opt/homebrew pip install --force-reinstall --no-binary pygrib pygrib
```
This assumes that you have used homebrew to install the eccodes library
***

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
