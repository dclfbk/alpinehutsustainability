This directory contains the majority of the data and intermediate data files used for the analysis. 

**Not listed**: large and/or private files → large files (such as DEM) can be downloaded locally using the scripts. 

The following table summarizes the organization of the data:

| Dir | Name  | Description  | Source | License  | Notes |
|---|---|---|---|---|---|
|  | alternatives_qnt.parquet  | Input for MCDM analysis with all criteria in quantitative form | `code/mcdm_analysis.ipynb` | -  | - |
| clip/ | *  | Polygon of Trentino  | [Geocatalogo PAT](https://siat.provincia.tn.it/geonetwork/srv/ita/catalog.search#/metadata/p_TN:377793f1-1094-4e81-810e-403897418b23) | CC0 1.0 Universal  | Used for clipping maps |
| graphs/ | *  | Edges, nodes and final trail graphs  | `code/trails_to_huts.ipynb` | -  | Intermediate files used for accessibility analysis |
| huts/ |  Rifugi_e_Bivacchi.* | Huts (SAT and privates) and bivouacs in Trentino | [GeocatalogoPAT](https://siat.provincia.tn.it/geonetwork/srv/ita/catalog.search#/metadata/p_TN:8ccc0bfb-ec39-4b5e-8af3-625c2c3b47cd) | CC0 1.0 Universal | Point geometries |
| |catasto_rifugi.csv|Cadastral information for SAT's huts (cad. municipality and parcel codes) |created via [MobileKat](https://mobilekat.provincia.tn.it/mobilekat/indexd.html#splash)|-|Used to download parcels polygons|
||categorie\_rifugi.csv|Basic hut information |SAT|-|Combined with point geometries from Rifugi_e_Bivacchi.* |
||huts\_joined.geojson|Merged GeoDataFrame containing both points and polygons|`code/huts_download.ipynb`|-|-|
||huts_parcels_downloaded.geojson|intermediate file with huts cadastal parcels after download|`code/huts_download.ipynb`|-|-|
||huts_points.geojson|standard_name + basic information + Point geometry (CRS:4326)|`code/huts_download.ipynb`|-|Combines huts/Rifugi_e_Bivacchi.* and huts/categorie_rifugi.csv|
||huts_points_32632.geojson|standard_name + basic information + Point geometry (CRS:32632)|`code/huts_download.ipynb`|-|Combines huts/Rifugi_e_Bivacchi.* and huts/categorie_rifugi.csv|
||huts_polygons.geojson|standard_name + cadastral polygons and centroids (CRS:4326)|`code/huts_download.ipynb`|-|-|
| maps/ | maps_large/SCD* , maps_large/SCF* | Snow Cover raster maps | `code/modis_maps.ipynb` | -  | Used in `code/maps.ipynb` |
|  | maps_large/WP*  | Tests of output Water Availability Map  | `code/maps.ipynb` | -  | - |
| others/ | buffer_2300m.gejson  | Buffer geometry  | `code/mcdm_analysis.ipynb` | -  | For QGIS visualizations |
|  | connected_goods.geojson  | Goods aerialways connected to huts  | `code/mcdm_analysis.ipynb` | -  | For QGIS visualizations |
| | connected_lifts.geojson | Visitor lifts connected to huts  | `code/mcdm_analysis.ipynb` | -  | For QGIS visualizations |
| | goods_aerialways.geojson | All goods aerialways | OpenStreetMap (OSM) [Tag:aerialway=goods](https://wiki.openstreetmap.org/wiki/Tag%3Aaerialway%3Dgoods) | Open Data Commons (ODbL) | - |
| | lifts_aerialways.geojson | All visitors lifts/aerialways | OpenStreetMap (OSM) [Tag:aerialway=[’station’, ’cable car’, ’chair lift’, ’gondola’, ’mixed lift’]](https://wiki.openstreetmap.org/wiki/Key:aerialway) | Open Data Commons (ODbL) | - |
| trails/ | Sentieri_della_SAT.*  | Hiking trails  | [Geocatalogo PAT](https://siat.provincia.tn.it/geonetwork/srv/ita/catalog.search#/metadata/p_TN:f3547bc8-bf1e-4731-85d2-2084d1f4ba07) | CC0 1.0 Universal  | - |
| water/ | carta_ris_idriche/pup_as/ , carta_ris_idriche/pup_so/ , carta_ris_idriche/pup_po/| Surface water (pup_as); water springs’ (pup_so); water-wells’ (pup_po) | [Carta Risorse Idriche PAT](https://www.provincia.tn.it/Documenti-e-dati/Documenti-di-supporto/Download-shapefile-Carta-delle-Risorse-idriche) | -  | Used in `code/maps.ipynb` |
|  | corpi_fluv/  | Major rivers  | [Corpi Idrici Fluviali PTA](https://siat.provincia.tn.it/geonetwork/srv/ita/catalog.search#/metadata/p_TN:df06e63c-d0f3-46c9-8ec2-c25a22c50ef7) | CC BY 4.0  | Used in `code/maps.ipynb` |
|  | corpi_laghi/  | Major lakes  | [Corpi Idrici Lacustri PTA](https://siat.provincia.tn.it/geonetwork/srv/ita/catalog.search#/metadata/p_TN:6137f8f2-cb30-4eb3-b533-181bd02619b8) | CC BY 4.0  | Used in `code/maps.ipynb` |
|  | corpi_sott/  | Major hydrogeologic areas  | [Corpi Idrici Sotterranei PTA](https://siat.provincia.tn.it/geonetwork/srv/ita/catalog.search#/metadata/p_TN:e701c6e4-4d6f-475f-ae08-8d37eba35248) | CC BY 4.0  | - |
|  | derivazioni/  | Active water catchments  | [Derivazioni Idriche Attive PAT](https://siat.provincia.tn.it/geonetwork/srv/ita/catalog.search#/metadata/p_TN:0ee6892f-280f-4119-924b-2c37dd71e275) | CC0 1.0  | Used in `code/maps.ipynb`  |
|  | glaciers2015/  | Glaciers in Trentino (2015)  | [Geocatalogo PAT](https://siat.provincia.tn.it/geonetwork/srv/ita/catalog.search#/metadata/p_TN:4b5b287f-cdce-4c9f-99f4-434b123d3d49) | CC0 1.0  | Used in `code/maps.ipynb`  |
