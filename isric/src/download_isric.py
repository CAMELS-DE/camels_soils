import os
from owslib.wcs import WebCoverageService

import geopandas as gpd
import rasterio


def download_isric_data(catchments: gpd.GeoDataFrame):
    """
    Download ISRIC data from the WCS server if it does not already exist
    and save to `/in/isric`.
    
    """
    # Variables to download
    variables = ["sand", "silt", "clay", "bdod", "cfvo", "soc"]

    # Bounding box of catchments +- a 10% buffer
    min_x, min_y, max_x, max_y = catchments.total_bounds
    buffer_width, buffer_height = (max_x - min_x) * 0.1, (max_y - min_y) * 0.1
    min_x, min_y, max_x, max_y = min_x - buffer_width, min_y - buffer_height, max_x + buffer_width, max_y + buffer_height

    # Only download for bounding box
    subsets = [('X', min_x, max_x), ('Y', min_y, max_y)]

    # Loop through the variables and download the data if it does not exist yet
    for variable in variables:
        # Depths to download
        depths = ["0-5cm", "5-15cm", "15-30cm", "30-60cm", "60-100cm", "100-200cm"]

        # Depths that do not need to be downloaded again
        depths_no_download = []

        for depth in depths:
            # path to the tiff file
            path = f"/in/isric/{variable}/{variable}_{depth}_mean.tiff"

            # check if data for the variable already exists
            if os.path.exists(path):
                with rasterio.open(path) as isric:
                    # check if the bounding box of the catchments is within the bounding box of the dem_merged.tif
                    if min_x >= isric.bounds.left and max_x <= isric.bounds.right and min_y >= isric.bounds.bottom and max_y <= isric.bounds.top:
                        # add the depth to the depths_no_download list
                        depths_no_download.append(depth)
                    else:
                        # remove the existing file
                        os.remove(path)
                        print(f"Removed existing file {path} as it does not cover the input catchments.")

        # remove the depths that do not need to be downloaded
        depths = [depth for depth in depths if depth not in depths_no_download]

        if depths_no_download:
            print(f"{variable} --- Data already exists and covers the input catchments, skipping download of {[f'{variable}_{depth}.tiff' for depth in depths_no_download]}.")

        # check if there are any depths to download
        if not depths:
            continue

        # start the WCS service
        wcs = WebCoverageService(f"http://maps.isric.org/mapserv?map=/map/{variable}.map", version="2.0.1")

        # get the coverage ids, only load the mean (there is also percentiles and uncertainty)
        coverage_ids = [content for content in wcs.contents if variable in content and "mean" in content]

        # filter the coverage ids by the depths
        coverage_ids = [coverage_id for coverage_id in coverage_ids if any(depth in coverage_id for depth in depths)]

        # create the variable folder to store .tiffs if it does not exist
        if not os.path.exists(f"/in/isric/{variable}"):
            os.makedirs(f"/in/isric/{variable}")

        for coverage_id in coverage_ids:            
            # get the response
            response = wcs.getCoverage(
                identifier=[coverage_id], 
                crs="http://www.opengis.net/def/crs/EPSG/0/152160",
                subsets=subsets, 
                resx=250, resy=250, 
                format="image/tiff")
            
            # save the tiff file
            with open(f"/in/isric/{variable}/{coverage_id}.tiff", "wb") as file:
                file.write(response.read())

        print(f"{variable} --- Downloaded {[coverage_id + '.tiff' for coverage_id in coverage_ids]}")


if __name__ == "__main__":
    from json2args.data import get_data_paths

    # get data paths
    data_paths = get_data_paths()

    # read catchments
    catchments = gpd.read_file(data_paths["catchments"])

    # transform catchments to the crs of the ISRIC data
    crs_isric = 'PROJCS["Interrupted_Goode_Homolosine",GEOGCS["WGS 84",DATUM["WGS_1984",SPHEROID["WGS 84",6378137,298.257223563,AUTHORITY["EPSG","7030"]],AUTHORITY["EPSG","6326"]],PRIMEM["Greenwich",0],UNIT["Degree",0.0174532925199433]],PROJECTION["Interrupted_Goode_Homolosine"],UNIT["metre",1,AUTHORITY["EPSG","9001"]],AXIS["Easting",EAST],AXIS["Northing",NORTH]]'
    catchments = catchments.to_crs(crs_isric)

    # download ISRIC data
    download_isric_data(catchments)

    # set permissions
    os.system("chmod -R 777 /in/isric")