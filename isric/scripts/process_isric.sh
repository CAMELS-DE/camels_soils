#!/bin/bash
# make directories to store the output data if they do not exist
mkdir -p /output_data/scripts

# logging
exec > >(tee -a /output_data/scripts/processing.log) 2>&1

# Start processing
echo "[$(date +%F\ %T)] Starting processing of ISRIC soil data for the CAMELS-DE dataset..."

# Download ISRIC soil data
echo "[$(date +%T)] Downloading ISRIC soil data..."
python /scripts/00_download_isric_data.py
cp /scripts/00_download_isric_data.py /output_data/scripts/00_download_isric_data.py
echo "[$(date +%T)] Downloaded and saved ISRIC soil data with 00_download_isric_data.py"

# Generate catchments geopackage
echo "[$(date +%T)] Generating MERIT Hydro catchments geopackage..."
python /scripts/01_generate_catchments_gpkg.py
cp /scripts/01_generate_catchments_gpkg.py /output_data/scripts/01_generate_catchments_gpkg.py
echo "[$(date +%T)] Saved MERIT Hydro geopackage for all CAMELS-DE stations with 01_generate_catchments_gpkg.py"

# Extract ISRIC data
echo "[$(date +%T)] Extracting ISRIC soil data..."
Rscript /scripts/02_extract_isric.R
cp /scripts/02_extract_isric.R /output_data/scripts/02_extract_isric.R
echo "[$(date +%T)] Saved extracted ISRIC soil data for all CAMELS-DE stations with 02_extract_isric.R"

# Postprocess extracted ISRIC data
echo "[$(date +%T)] Postprocessing extracted ISRIC soil data..."
python /scripts/03_postprocess_isric.py
cp /scripts/03_postprocess_isric.py /output_data/scripts/03_postprocess_isric.py
echo "[$(date +%T)] Saved postprocessed ISRIC soil data for all CAMELS-DE stations with 03_postprocess_isric.py"

# Copy the output data to the camelsp output directory
echo "[$(date +%T)] Copying the extracted and postprocessed data to the camelsp output directory..."
mkdir -p /camelsp/output_data/raw_catchment_attributes/soils/isric
cp -r /output_data/isric_processed/* /camelsp/output_data/raw_catchment_attributes/soils/isric/
echo "[$(date +%T)] Copied the extracted and postprocessed data to the camelsp output directory"

# Copy scripts to /camelsp/output_data/scripts/catchments
mkdir -p /camelsp/output_data/scripts/soils/isric/
cp /output_data/scripts/* /camelsp/output_data/scripts/soils/isric/

# Change permissions of the output data
chmod -R 777 /camelsp/output_data/
chmod -R 777 /output_data/
chmod -R 777 /input_data/