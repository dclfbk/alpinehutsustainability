## Script containing functions to use in other files 
import os
import requests
import zipfile
import rasterio

## DATA DOWNLOAD & PREPROCESSING
def download_and_unzip_shapefile(url, extract_to='../data/', download=True):
    ''' Parameters:
        - url: access url for download OR file path for zip extraction
        - extract to: destination path
        - download: download if True, only extract if False

        Returns: string message with destination path. 
    '''

    if not os.path.exists(extract_to):
        os.makedirs(extract_to)

    if download:
        # Download the file
        local_zip_file = os.path.join(extract_to, 'shapefile.zip')
        with requests.get(url, stream=True) as r:
            with open(local_zip_file, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
    
    elif not download:
        local_zip_file = url
        
    # Extract the file
    with zipfile.ZipFile(local_zip_file, 'r') as zip_ref:
        zip_ref.extractall(extract_to)

    os.remove(local_zip_file)
    
    # Return the path to the directory containing the shapefiles
    return print(f'Shapefile ready in {extract_to}')


def standardize_name(name:str):
    ''' Converts names to lowercase, strips leading and trailing whitespace, 
    and removes non-alphanumeric characters.
    '''
    return ''.join(e for e in name.lower().strip() if e.isalnum())

## TERRITORIAL MAPS CREATION
def save_raster_map(raster, dem_profile, filename, destination_dir = '../data/maps/'):
    os.makedirs(destination_dir, exist_ok=True)
    output_profile = dem_profile
    output_profile.update(dtype=rasterio.float32, count=1)

    with rasterio.open(destination_dir + f"{filename}.tif", 'w', **output_profile) as dst:
        dst.write(raster, 1)