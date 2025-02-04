### Data Download & Preprocessing
- `huts_download.ipynb`: huts basic info and geometries.
- `water_download.ipynb`: water resources data (rivers, derivations, glaciers, etc.).
- `others_download.ipynb`: terrain (DEM, slope), hiking trails, aerialways and lifts. 
- `modis_download.py`: MODIS Snow Cover. Tested in `modis_download.ipynb`. 
- `modis_maps.ipynb`: computation of Snow Cover Duration (SCD) and Snow Cover Frequency (SCF) maps for snowfall season, melting season and late summer.

### Analysis
Main:
- `mcdm_analysis.ipynb`: notebook for the huts MCDM evaluation. Steps: (1) Creation of *alternatives* dataset (2) Conversion of qualitative criteria (3) Weights and methods selection (4) Ranks computation (5) Analysis of results.
- `maps.ipynb`: notebook for creation of Water Availability Map. Steps: (1) Creation of individual *source raster maps*, normalized (2) Aggregation using WCL (Weighted Linear Combination) (3) Save results in raster file for visualization in QGIS.
- `cluster_analysis.ipynb`: perform K-means clustering on (1) huts' topographic features and (2) on huts' rankings.

Others:
- `trails_to_huts.ipynb`: analysis of accessibility of huts (validation of CAI/SAT category).
- `study_area.ipynb`: study area exploration and huts' criteria overview.
- `functions.py`: helper functions called in the scripts above.