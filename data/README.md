| dir | name  | url/source  | description  | license  | note |
|---|---|---|---|---|---|
| huts/ |  Rifugi_e_Bivacchi.* | [GeocatalogoPAT](https://siat.provincia.tn.it/geonetwork/srv/ita/catalog.search#/metadata/p_TN:8ccc0bfb-ec39-4b5e-8af3-625c2c3b47cd)  | shapefile about huts (SAT and privates) and bivouacs in Trentino  | must check | Point geometries |
|huts/ |catasto_rifugi.csv|created via [MobileKat](https://mobilekat.provincia.tn.it/mobilekat/indexd.html#splash)|cadastral information for SAT's huts (cad. municipality and parcel codes)|---|used to download parcels polygons|
|huts/|categorie_rifugi.csv|SAT's dataset|hut categories (ABCD, Esc/Alp), elevation, number of beds|---|combined with point geometries from Rifugi_e_Bivacchi.* |
|huts/|huts_joined.geojson|`code/huts_download.ipynb`|old solution containing both points and polygons|---|may not use|
|huts/|huts_parcels_downloaded.geojson|`code/huts_download.ipynb`|intermediate file with huts cadastal parcels after download|---|---|
|huts/|huts_points.geojson|`code/huts_download.ipynb`|standard_name + basic information + Point geometry|---|aggregates huts/Rifugi_e_Bivacchi.* and huts/categorie_rifugi.csv|
|huts/|huts_polygons.geojson|`code/huts_download.ipynb`|standard_name + cadastral polygons and centroids|---|---|
