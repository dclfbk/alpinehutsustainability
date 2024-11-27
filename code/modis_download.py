import earthaccess
import os
import xarray as xr
import numpy as np
from io import BytesIO
import tempfile
from pyhdf.SD import *
import re
from pyproj import Transformer
import concurrent.futures
import rasterio
import time
from itertools import islice

import logging
logger = logging.getLogger(__name__)  


def process_granule(hdf, output_path, studyarea_bbox_4326=[10.46750857, 45.69873184, 11.94937569, 46.53633029]):
    ''' Function to process granule saved on tmp file:
        - verify data quality (Basic_QA and Cloud Persistence) for the studyarea
        - if valid, crop all datasets (NDSI) and save to local hdf file

        Parameters:
        - hdf: granule hdf file (SD istance) to process
        - output_path: filename for saving new hdf file
        - studyarea_bbox_4326: bbox of study area (EPSG:4326)
    '''
    # Get geo metadata from file
    geo_md = get_geomd(hdf)
    # Load transformer
    transf_coords = load_transformer(studyarea_bbox_4326)    

    logger.info('Checking pixel quality...')
    # Check Basic_QA (quality)
    if not verify_validrange(hdf.select('Basic_QA'), 
                             extract_study_area(hdf, 'Basic_QA', studyarea_bbox_4326, geo_md, transf_coords)):
        logger.warning("Granule failed Pixel Quality check.")
        return

    # Check Cloud_Persistence?
    if not verify_validrange(hdf.select('Cloud_Persistence'), 
                             extract_study_area(hdf, 'Cloud_Persistence', studyarea_bbox_4326, geo_md, transf_coords)):
        logger.warning("Granule failed Cloud Persistence check.")
        return

    # Crop all datasets and save to new local HDF4 
    #output_path = extract_and_save_datasets(hdf, output_path, studyarea_bbox_4326, geo_md, transf_coords) 
    output_tif = save_dataset_tif(hdf, 'CGF_NDSI_Snow_Cover', output_path, geo_md, transf_coords, studyarea_bbox_4326)

    return output_tif

def load_transformer(
    studyarea_bbox_4326:list,
    studyarea_crs = "EPSG:4326",
    modis_crs = "+proj=sinu +lon_0=0 +x_0=0 +y_0=0 +a=6371007.181 +b=6371007.181 +units=m +no_defs", # sinusoidal
    ):
    ''' Load transformer studyarea --> MODIS. Used in func extract_study_area()'''
    transformer = Transformer.from_crs(studyarea_crs, modis_crs)
    min_x, min_y = transformer.transform(studyarea_bbox_4326[1], studyarea_bbox_4326[0])  # (lat, lon)
    max_x, max_y = transformer.transform(studyarea_bbox_4326[3], studyarea_bbox_4326[2])  

    return {'min_x':min_x, 'min_y':min_y, 'max_x':max_x, 'max_y':max_y}

def extract_study_area(hdf, ds_name, studyarea_bbox_4326:list, geo_md:dict, transf_coords:dict): 
    ''' Crop dataset to select only study area. 
    
    Parameters:
    - hdf: hdf granule file
    - ds_name: name of dataset to crop
    - studyarea_bbox_4326: bbox of study area (WGS84-EPSG:4326). Default is bbox for Trentino.
    - geo_md: dict of geo metadata.
    - transf_coords: dict of transformed studyarea bbox coordinates.
    
    Returns:
    - cropped_data: np.ndarray containing cropped data. '''

    # Unpack geo metadata
    granule_bbox_sinu = geo_md['granule_bbox']
    res_x = geo_md['resolution_x']
    res_y = geo_md['resolution_y']
    # Unpack transf bbox coords
    min_x, min_y = transf_coords['min_x'], transf_coords['min_y']
    max_x, max_y = transf_coords['max_x'], transf_coords['max_y']

    # Clip the transformed bounding box to the granule bounding box
    min_x = max(min_x, granule_bbox_sinu[0])
    min_y = max(min_y, granule_bbox_sinu[1])
    max_x = min(max_x, granule_bbox_sinu[2])
    max_y = min(max_y, granule_bbox_sinu[3])

    # Calculate pixel coordinates
    row_min = int((granule_bbox_sinu[3] - max_y) / res_y)  # Y-axis origin is at the top
    row_max = int((granule_bbox_sinu[3] - min_y) / res_y)
    col_min = int((min_x - granule_bbox_sinu[0]) / res_x)
    col_max = int((max_x - granule_bbox_sinu[0]) / res_x)

    # Subset data using indexes
    full_data = hdf.select(ds_name).get() 
    cropped_data = full_data[row_min:row_max, col_min:col_max]

    assert cropped_data.shape != 0, f"Cropped data for {ds_name} is empty. Check bounding box."
    return cropped_data

def get_geomd(hdf):
    ''' Recover granule geographic metadata.
    
    Parameters:
    - hdf: hdf granule file
    
    Returns: dict containing
        - granule_bbox: bbox of file (sinusoidal proj)
        - resolution_x, resolution_y: pixel resolution (meters)
        - x_dim, y_dim: grid dimensions (pixels) '''

    glob_attributes = hdf.attributes()
    if 'StructMetadata.0' in glob_attributes:
        struct_metadata = glob_attributes['StructMetadata.0']
        #print("--> Extracting geo metadata...")
    else:
        raise KeyError("Attribute StructMetadata.0 not found.")
    
    # Extract upper-left and lower-right coordinates in meters (regex search)
    upper_left = re.search(r"UpperLeftPointMtrs=\((-?\d+\.?\d*),\s*(-?\d+\.?\d*)\)", struct_metadata)
    lower_right = re.search(r"LowerRightMtrs=\((-?\d+\.?\d*),\s*(-?\d+\.?\d*)\)", struct_metadata)
    x_dim = re.search(r"XDim=(\d+)", struct_metadata)
    y_dim = re.search(r"YDim=(\d+)", struct_metadata)

    if upper_left and lower_right:
        ul_x, ul_y = map(float, upper_left.groups())
        lr_x, lr_y = map(float, lower_right.groups())
        granule_bbox = [ul_x, lr_y, lr_x, ul_y]
        x_dim, y_dim = int(x_dim.group(1)), int(y_dim.group(1))
        # Resolution
        resolution_x = (lr_x - ul_x) / x_dim
        resolution_y = (ul_y - lr_y) / y_dim
    
    geo_md = {'granule_bbox': granule_bbox,
                    'resolution_x': resolution_x,
                    'resolution_y': resolution_y,
                    'x_dim': x_dim,
                    'y_dim': y_dim}

    return geo_md

def verify_validrange(dataset, data, valid_thr=95):
    ''' Check valid percentage of data. '''

    valid_range = dataset.attributes()["valid_range"]
    if len(valid_range) != 2:
        raise ValueError("valid_range attribute should have exactly two elements.")

    # Mask for values within the valid range
    valid_min, valid_max = valid_range
    valid_mask = (data >= valid_min) & (data <= valid_max)

    # Calculate the percentage of valid values
    valid_percentage = np.sum(valid_mask) / data.size * 100

    # Check if at least valid_thr of the values are valid
    if valid_percentage >= valid_thr:
        return True
    else:
        logger.warning(f"Warning: Only {valid_percentage:.2f}% within the valid range.")
        return False

def verify_missingdata(dataset, data, valid_thr=95):
    ''' Check missing data percentage '''

    # Create dict of data values
    keys_str = dataset.attributes()['Key']   
    pairs = [item.strip() for item in keys_str.split(',')]
    data_dict = {}
    for pair in pairs:
        value, key = pair.split('=')
        key = key.replace(' ', '_')
        try:
            data_dict[key.strip()] = int(value.strip())
        except ValueError:
            # valid data range 
            data_dict[key.strip()] = value.strip()

    missingdata_count = np.sum(data == data_dict['missing_data'])
    fill_count = np.sum(data == data_dict['fill'])
    na_count = missingdata_count + fill_count
    missingdata_percentage = na_count / data.size * 100

    if missingdata_percentage < valid_thr:
        return True
    else:
        logger.warning(f"Warning: {missingdata_percentage}% missing data.")
        return False

def extract_and_save_datasets(hdf, output_path, studyarea_bbox_4326:list, geo_md:dict, transf_coords:dict): 

    ''' Extracts all datasets in hdf tmpfile for the study area,
    then writes them in a local hdf file. '''

    # Data types of class pyhdf.SD.SDC
    hdf4_type_mapping = {
        4: SDC.CHAR,     # 8-bit character
        4: SDC.CHAR8,    # 8-bit character
        3: SDC.UCHAR,    # unsigned 8-bit integer
        3: SDC.UCHAR8,   # unsigned 8-bit integer
        20: SDC.INT8,    # signed 8-bit integer
        21: SDC.UINT8,   # unsigned 8-bit integer
        22: SDC.INT16,   # signed 16-bit integer
        23: SDC.UINT16,  # unsigned 16-bit intege
        24: SDC.INT32,   # signed 32-bit integer
        25: SDC.UINT32   # unsigned 32-bit integer
    }

    print("--> Extracting & saving all datasets to new HDF4 file...")
    new_hdf = SD(output_path, SDC.WRITE | SDC.CREATE)
    for ds_name in hdf.datasets():
        print(f"-> Exctracting dataset: {ds_name}")
        ds = hdf.select(ds_name)
        cropped_data = extract_study_area(hdf, ds_name, studyarea_bbox_4326, geo_md, transf_coords) 
        # Check missing data for NDSI datasets
        if ds_name in ['CGF_NDSI_Snow_Cover', 'MOD10A1_NDSI_Snow_Cover']:
            valid = verify_missingdata(ds, cropped_data)
            if not valid:
                return print(f"Warning! {ds_name} failed missing data check.")

        # Create a new dataset in the output file
        data_type = hdf4_type_mapping.get(ds.info()[3])
        dims = cropped_data.shape
        new_ds = new_hdf.create(ds_name, data_type, dims)
        
        # Copy attributes
        for attr_name in ds.attributes():
            setattr(new_ds, attr_name, ds.attributes()[attr_name])

        # Write data
        new_ds[:] = cropped_data 
        print(f"New dataset shape: {cropped_data.shape}") 

    new_hdf.end()

    return output_path

def save_dataset_tif(hdf, ds_name, output_path, geo_md:dict, transf_coords:dict, studyarea_bbox_4326:list, data_crs="+proj=sinu +lon_0=0 +x_0=0 +y_0=0 +a=6371007.181 +b=6371007.181 +units=m +no_defs"):
    
    # Fix output file format
    granule_name = os.path.basename(output_path)
    name_as_list = granule_name.split('.')[:-1]
    name_as_list.append(ds_name)
    output_tif = os.path.dirname(output_path) + "/" + ".".join(name_as_list) + ".tif"
    
    # Extract dataset
    data = extract_study_area(hdf, ds_name, studyarea_bbox_4326, geo_md, transf_coords) 
    # Check missing data for NDSI datasets
    if ds_name in ['CGF_NDSI_Snow_Cover', 'MOD10A1_NDSI_Snow_Cover']:
        if not verify_missingdata(hdf.select(ds_name), data):
            logger.warning(f"Warning! {ds_name} failed missing data check.")
            return 
            
    # Define transform (top-left corner of cropped area)
    if data_crs == 'EPSG:4326':  # WGS84
        min_x, max_y = studyarea_bbox_4326[0], studyarea_bbox_4326[3]
    else: # sinusoidal
        min_x, max_y = transf_coords['min_x'], transf_coords['max_y']

    res_x, res_y = geo_md['resolution_x'], geo_md['resolution_y']
    transform = rasterio.transform.from_origin(min_x, max_y, res_x, res_y)  # affine transform

    # Save the cropped data as GeoTIFF
    with rasterio.open(
        output_tif,
        'w',
        driver='GTiff',
        height=data.shape[0],
        width=data.shape[1],
        count=1,  # Single band
        dtype=data.dtype,
        crs=data_crs,
        transform=transform,
    ) as dst:
        dst.write(data, 1)  # Write to the first (and only) band

    return output_tif

## PARALLEL PROCESSING
def ensure_directory_exists(directory_path):
    if not os.path.exists(directory_path):
        try:
            os.makedirs(directory_path)
            print(f"Output directory created: {directory_path}")
        except OSError as e:
            logger.critical(f"Error creating directory {directory_path}: {e}")
    else:
        print(f"Output directory already exists: {directory_path}")

def process_single_granule(granule, output_dir, studyarea_bbox_4326):
    """Function to process a single granule."""

    output_tif = None

    try:
        granule_name = os.path.basename(granule.full_name)
        output_path = os.path.join(output_dir, granule_name)

        # Load in-memory file
        with BytesIO(granule.read()) as in_memory_file:
            header = in_memory_file.read(8)  # First 8 bytes to identify format
            logger.debug(f"Header bytes for granule {granule_name}: {header}")
            
            if header.startswith(b'\x0e\x03'):  # HDF4
                with tempfile.NamedTemporaryFile(suffix=".hdf", delete=True) as tmp_file:
                    tmp_file.write(in_memory_file.getvalue())
                    tmp_file.flush()
                    logger.debug(f"Temporary HDF file created for granule: {granule_name}")

                    # Open the HDF4 file
                    hdf = SD(tmp_file.name, SDC.READ)
                    if hdf.datasets():
                        logger.info(f"\PROCESSING GRANULE: {granule_name}")
                        output_tif = process_granule(hdf, output_path, studyarea_bbox_4326)
                    else:
                        logger.warning(f"No datasets found in granule: {granule_name}")
            else:
                logger.warning(f"Unknown file format for granule: {granule_name}")

    except Exception as e:
        logger.critical(f"Error processing granule {granule_name}: {e}")

    if output_tif is None:
        logger.warning(f"Processing for granule {granule_name} did not produce an output file.")

    return output_tif

def process_all_granules_in_parallel(granules, output_dir, max_workers=4, studyarea_bbox_4326=[10.46750857, 45.69873184, 11.94937569, 46.53633029]):
    """Process all granules using parallel processing."""
    
    success_count = 0
    failed_granules = []

    # Use ProcessPoolExecutor for parallel processing
    with concurrent.futures.ProcessPoolExecutor(max_workers=max_workers) as executor:
        # Submit tasks
        futures = {
            executor.submit(process_single_granule, granule, output_dir, studyarea_bbox_4326): granule
            for granule in granules
        }

        # Collect results
        for future in concurrent.futures.as_completed(futures):
            granule = futures[future]
            try:
                result = future.result()
                if result == None: # failed
                    logger.info(f"Granule with None output: {granule.full_name}")
                    failed_granules.append(granule.full_name)
                else:    
                    logger.info(f"Granule processed and saved to: {result}")
                    success_count +=1
            except Exception as e:
                logger.critical(f"Granule {granule.full_name} failed with error: {e}")
                failed_granules.append(granule.full_name)

    return success_count, failed_granules

## BATCH PROCESSING

def batch_generator(iterable, batch_size, initial_batch_size=2):  
    """ Yield successive batches from an iterable. 
    Uses a smaller batch size for the first batch request to avoid overloading errors. """
    it = iter(iterable)
    first_batch = True
    while True:
        batch = list(islice(it, batch_size if not first_batch else initial_batch_size))
        first_batch = False
        if not batch:
            break
        yield batch

def process_granules_with_batches(granules, output_dir, batch_size, max_workers=4, studyarea_bbox_4326=[10.46750857, 45.69873184, 11.94937569, 46.53633029]):
    """Process granules in batches."""
    total_success = 0
    total_batches = (len(granules) + batch_size - 1) // batch_size

    logger.info(f"Starting processing for {len(granules)} granules in {total_batches} batches (batch size: {batch_size}).")
    
    for batch_num, batch in enumerate(batch_generator(granules, batch_size), start=1):
        logger.info(f"\nPROCESSING BATCH {batch_num}/{total_batches} with {len(batch)} granules...")
        
        # Process batch
        success_count, failed_granules = process_all_granules_in_parallel(batch, output_dir, max_workers, studyarea_bbox_4326)
        
        logger.info(f"Batch {batch_num} completed. {success_count} granules successfully processed.")
        total_success += success_count

    logger.info(f"All batches completed")
    logger.info(f"Successfully processed granules: {total_success}/{len(granules)}")
    if failed_granules:
        logger.warning(f"Failed granules ({len(failed_granules)}/{len(granules)}): \n{failed_granules}")



if __name__ == '__main__':
    TEMPORAL_RANGE = ("2021-10-01", "2024-10-01")
    BBOX_4326 = (10.46750857, 45.69873184, 11.94937569, 46.53633029) # TRENTINO EPSG:4326
    OUTPUT_DIR = "/Volumes/TOSHIBA_EXT/MODIS_RASTERS"
    BATCH_SIZE = 15

    # Set up logging configuration
    logging.basicConfig(
        level=logging.INFO,  # Default log level
        format='%(asctime)s - %(levelname)s - %(message)s',  
        handlers=[
            logging.FileHandler("modis_download.log", mode="w"),  
            logging.StreamHandler()  # show on the console
        ]
    )

    start_time = time.time()
    # Step 1: login (uses credentials in .netcr file)
    session = earthaccess.login()
    logger.info('Authentication completed.')

    # Step 2: search for data
    results = earthaccess.search_data(
        short_name = "MOD10A1F", # dataset
        version = "61",
        bounding_box = BBOX_4326,
        temporal = TEMPORAL_RANGE,
        count = -1 # all
    )
    logger.info('Data search completed. Starting extraction...')

    # Step 3: preprocess and download
    granules = earthaccess.open(results) # (list of file-like objects)
    ensure_directory_exists(OUTPUT_DIR)
    process_granules_with_batches(granules, OUTPUT_DIR, batch_size=BATCH_SIZE)

    # Final logs
    end_time = time.time()
    total_seconds = end_time - start_time
    hours, remainder = divmod(total_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    logger.info(f"Total computation time: {int(hours)}:{int(minutes)}:{seconds:.2f}")
    logger.info(f"Total computation time: {(total_seconds):.2f} seconds")

    