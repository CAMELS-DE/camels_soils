library(exactextractr)
library(terra)
library(sf)


extract_isric <- function(catchments, id_field_name_catchments) {
  # Load catchment polygons
  print(paste("Loading catchment polygons from", catchments, "..."))
  catchments <- sf::st_read(catchments)

  # List of variables
  variables <- c("sand", "silt", "clay", "bdod", "cfvo", "soc")

  # depths
  depths <- c("0-5cm", "5-15cm", "15-30cm", "30-60cm", "60-100cm", "100-200cm")

  # Loop over the variables
  for (variable in variables) {
    # Loop over the depths and extract the data
    for (depth in depths) {
      # Load the ISRIC raster
      filename <- paste("/in/isric/", variable, "/", variable, "_", depth, "_mean.tiff", sep = "")
      isric <- terra::rast(filename)

      # Transform catchments to match the raster coordinate system
      catchments <- sf::st_transform(catchments, sf::st_crs(isric))

      # Statistics to calculate
      stats <- c("mean", "min", "max", "quantile", "stdev")

      # Extract the raster data for all catchments
      extracted_rast <- exactextractr::exact_extract(isric, catchments, fun = stats, quantiles = c(0.05, 0.5, 0.95), 
                                                     append_cols = id_field_name_catchments, progress = FALSE)

      # Rename id column
      colnames(extracted_rast)[1] <- "gauge_id"

      # Create folder to save the extracted data if it does not exist
      dir.create(paste("/out/isric_extracted/", sep = ""), showWarnings = FALSE)
      dir.create(paste("/out/isric_extracted/", variable, sep = ""), showWarnings = FALSE)

      # Save the extracted data
      write.csv(extracted_rast, paste("/out/isric_extracted/", variable, "/", "isric_", variable, "_", depth, "_extracted.csv", sep = ""), row.names = FALSE)
    }
  print(paste(variable, "--- Extraction successful."))
  }
}
