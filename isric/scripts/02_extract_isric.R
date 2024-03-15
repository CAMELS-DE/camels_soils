# Calculate statistics of ISRIC soil data for catchment polygons (from gpkg).
# @author: Alexander Dolich
#
# created: 2024/03/04
# modified: 2024/03/04

library(exactextractr)
library(terra)
library(sf)


# Load catchment polygons
print("Loading catchment polygons from /output_data/catchments.gpkg ...")
catchments <- sf::st_read("/output_data/catchments.gpkg")

# List of variables
variables <- c("sand", "silt", "clay", "bdod", "cfvo", "soc")

# depths
depths <- c("0-5cm", "5-15cm", "15-30cm", "30-60cm", "60-100cm", "100-200cm")

# Loop over the variables
for (variable in variables) {
  # Load the ISRIC raster
  print(paste("Start processing variable", variable, "..."))

  # Loop over the depths and extract the data
  for (depth in depths) {
    filename <- paste("/input_data/isric/", variable, "/", variable, "_", depth, "_mean.tiff", sep = "")
    isric <- terra::rast(filename)

    # Transform catchments to match the raster coordinate system
    catchments <- st_transform(catchments, st_crs(isric))

    # Statistics to calculate
    stats <- c("mean", "min", "max", "quantile", "stdev")

    # Extract the raster data for all catchments
    print(paste("Extracting the raster data for all catchments for variable", variable, "and depth", depth, "..."))
    extracted_rast <- exact_extract(isric, catchments, fun = stats, quantiles = c(0.05, 0.5, 0.95),
                                    append_cols = "id", progress = FALSE)

    # Rename id column
    colnames(extracted_rast)[1] <- "camels_id"

    # Create folder to save the extracted data if it does not exist
    dir.create(paste("/output_data/isric_extracted/", sep = ""), showWarnings = FALSE)
    dir.create(paste("/output_data/isric_extracted/", variable, sep = ""), showWarnings = FALSE)

    # Save the extracted data
    print(paste("Saving the extracted data to /output_data/isric_extracted/", variable, "/", "isric_", variable, "_", depth, "_extracted.csv ...", sep = ""))
    write.csv(extracted_rast, paste("/output_data/isric_extracted/", variable, "/", "isric_", variable, "_", depth, "_extracted.csv", sep = ""), row.names = FALSE)
  }
}