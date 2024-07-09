# load json2aRgs for parameter parsing
library(json2aRgs)

# load the extract_corine function
source("extract_isric.R")

# get the parameters for the tool
params <- get_parameters()

# # get the data paths for the tool
data <- get_data(return_data_paths = TRUE)

# check if a toolname was set in env
toolname <- tolower(Sys.getenv("TOOL_RUN"))

# if no toolname was set, stop the script
if (toolname == "") {
  stop("No toolname was set in the environment. Please set the TOOL_RUN environment variable.")

} else if (toolname == "soil_attributes_isric") {
  # run Python script to download the ISRIC SoilGrids data if it does not exist yet
  system("python3 /src/download_isric.py")

  # extract the ISRIC SoilGrids data
  extract_isric(catchments = data$catchments, 
                id_field_name_catchments = params$id_field_name_catchments)

  # postprocess and merge extracted data as in CAMELS-DE
  system("python3 /src/postprocess_isric.py")

} else {
  stop("The toolname '", toolname, "' is not supported.")
}