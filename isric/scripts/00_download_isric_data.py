import os
from owslib.wcs import WebCoverageService


def download_isric_data():
    """
    Download ISRIC data from the WCS server if it does not already exist.
    
    """
    # Variables to download
    variables = ["sand", "silt", "clay", "bdod", "cfvo", "soc"]

    # Depths to download
    depths = ["0-5cm", "5-15cm", "15-30cm", "30-60cm", "60-100cm", "100-200cm"]

    # Only download for Germany (+ buffer)
    subsets = [('X', 1347207, 2452109), ('Y', 5194990, 6082404)]

    # Loop through the variables and download the data
    for variable in variables:
        # start the WCS service
        wcs = WebCoverageService(f"http://maps.isric.org/mapserv?map=/map/{variable}.map", version="2.0.1")

        # get the coverage ids, only load the mean (there is also percentiles and uncertainty)
        coverage_ids = [content for content in wcs.contents if variable in content and "mean" in content]

        # filter the coverage ids by the depths
        coverage_ids = [coverage_id for coverage_id in coverage_ids if any(depth in coverage_id for depth in depths)]

        # create the variable folder to store .tiffs if it does not exist
        if not os.path.exists(f"/input_data/isric/{variable}"):
            os.makedirs(f"/input_data/isric/{variable}")

        for coverage_id in coverage_ids:
            # check if file already exists
            if os.path.exists(f"/input_data/isric/{variable}/{coverage_id}.tiff"):
                continue
            
            # get the response
            response = wcs.getCoverage(
                identifier=[coverage_id], 
                crs="http://www.opengis.net/def/crs/EPSG/0/152160",
                subsets=subsets, 
                resx=250, resy=250, 
                format="image/tiff")
            
            # save the tiff file
            with open(f"/input_data/isric/{variable}/{coverage_id}.tiff", "wb") as file:
                file.write(response.read())

        print(f"{variable} --- Downloaded {[coverage_id + '.tiff' for coverage_id in coverage_ids]}")


if __name__ == "__main__":
    download_isric_data()