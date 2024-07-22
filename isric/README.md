# ISRIC SoilGrids250m

## Description

Dockerized tool to extract and process data from the ISRIC Soil Grids tiff files for CAMELS-DE.  
A folder is created in the `output_data` folder for the results of each catchment, in which a .csv file is saved for each of the variables listed below. Output variables are weighted averages for the depths 0-30 cm, 30-100 cm and 100-200cm. Extracted variables are copied to the camelsp `output_data` directory, where other tools process the data further and organize it in the folder structure.

## Container

### Build the container

```bash
docker build -t isric .
```

### Run the container

Necessary Soild Grids input data is automatically downloaded when running the docker container.

To run the container, the local `input_data`, `output_data` and `camelsp/output_data` directories have to be mounted inside the container:

```bash
docker run -v ./input_data:/input_data -v ./output_data:/output_data -v /path/to/local/camelsp/output_data:/camelsp/output_data -it --rm isric
```

## Output variables

Various statistics such as min, mean, max, percentiles and standard deviation of the Soil Grids variables are calculated for the CAMELS-DE catchments.  
The tool uses Soil Grid variables in depths 0-5 cm, 5-15 cm, 15-30 cm, 30-60 cm, 60-100 cm and 100-200 cm; we aggregate the results to the two depths 0-30 cm, 30-100 cm and 100-200 cm by calculating a weighted average.   
Variables are then converted to the units used in CAMELS-DE as listed here:

| **Soil Grids variable** | **Soil Grids unit** | **CAMELS-DE conversion factor** | **CAMELS-DE unit** | **CAMELS-DE variable name** |
|-------------------------|---------------------|---------------------------------|--------------------|-----------------------------|
| bdod                    | cg/cm³              | 100                             | kg/dm³             | bulk_density                |
| cfvo                    | cm3/dm3 (vol‰)      | 10                              | cm3/100cm3 (vol%)  | coarse_fragments            |
| clay                    | g/kg                | 10                              | g/100g (%)         | clay                        |
| silt                    | g/kg                | 10                              | g/100g (%)         | silt                        |
| sand                    | g/kg                | 10                              | g/100g (%)         | sand                        |
| soc                     | dg/kg               | 10                              | g/kg               | soil_organic_carbon         |


**Bulk density of the fine earth fraction (bulk_density)**:
- bulk_density_0_30cm_mean [kg/dm³]
- bulk_density_0_30cm_min [kg/dm³]
- bulk_density_0_30cm_max [kg/dm³]
- bulk_density_0_30cm_q05 [kg/dm³]
- bulk_density_0_30cm_q50 [kg/dm³]
- bulk_density_0_30cm_q95 [kg/dm³]
- bulk_density_0_30cm_stdev [kg/dm³]
- bulk_density_30_100cm_mean [kg/dm³]
- bulk_density_30_100cm_min [kg/dm³]
- bulk_density_30_100cm_max [kg/dm³]
- bulk_density_30_100cm_q05 [kg/dm³]
- bulk_density_30_100cm_q50 [kg/dm³]
- bulk_density_30_100cm_q95 [kg/dm³]
- bulk_density_30_100cm_stdev [kg/dm³]
- bulk_density_100_200cm_mean [kg/dm³]
- bulk_density_100_200cm_min [kg/dm³]
- bulk_density_100_200cm_max [kg/dm³]
- bulk_density_100_200cm_q05 [kg/dm³]
- bulk_density_100_200cm_q50 [kg/dm³]
- bulk_density_100_200cm_q95 [kg/dm³]
- bulk_density_100_200cm_stdev [kg/dm³]

**Volumetric fraction of coarse fragments > 2 mm (coarse_fragments)**:
- coarse_fragments_0_30cm_mean [cm³/100cm³ (vol%)]
- coarse_fragments_0_30cm_min [cm³/100cm³ (vol%)]
- coarse_fragments_0_30cm_max [cm³/100cm³ (vol%)]
- coarse_fragments_0_30cm_q05 [cm³/100cm³ (vol%)]
- coarse_fragments_0_30cm_q50 [cm³/100cm³ (vol%)]
- coarse_fragments_0_30cm_q95 [cm³/100cm³ (vol%)]
- coarse_fragments_0_30cm_stdev [cm³/100cm³ (vol%)]
- coarse_fragments_30_100cm_mean [cm³/100cm³ (vol%)]
- coarse_fragments_30_100cm_min [cm³/100cm³ (vol%)]
- coarse_fragments_30_100cm_max [cm³/100cm³ (vol%)]
- coarse_fragments_30_100cm_q05 [cm³/100cm³ (vol%)]
- coarse_fragments_30_100cm_q50 [cm³/100cm³ (vol%)]
- coarse_fragments_30_100cm_q95 [cm³/100cm³ (vol%)]
- coarse_fragments_30_100cm_stdev [cm³/100cm³ (vol%)]
- coarse_fragments_100_200cm_mean [cm³/100cm³ (vol%)]
- coarse_fragments_100_200cm_min [cm³/100cm³ (vol%)]
- coarse_fragments_100_200cm_max [cm³/100cm³ (vol%)]
- coarse_fragments_100_200cm_q05 [cm³/100cm³ (vol%)]
- coarse_fragments_100_200cm_q50 [cm³/100cm³ (vol%)]
- coarse_fragments_100_200cm_q95 [cm³/100cm³ (vol%)]
- coarse_fragments_100_200cm_stdev [cm³/100cm³ (vol%)]

**Proportion of clay particles (< 0.002 mm) in the fine earth fraction (clay)**:
- clay_0_30cm_mean [g/100g (%)]
- clay_0_30cm_min [g/100g (%)]
- clay_0_30cm_max [g/100g (%)]
- clay_0_30cm_q05 [g/100g (%)]
- clay_0_30cm_q50 [g/100g (%)]
- clay_0_30cm_q95 [g/100g (%)]
- clay_0_30cm_stdev [g/100g (%)]
- clay_30_100cm_mean [g/100g (%)]
- clay_30_100cm_min [g/100g (%)]
- clay_30_100cm_max [g/100g (%)]
- clay_30_100cm_q05 [g/100g (%)]
- clay_30_100cm_q50 [g/100g (%)]
- clay_30_100cm_q95 [g/100g (%)]
- clay_30_100cm_stdev [g/100g (%)]
- clay_100_200cm_mean [g/100g (%)]
- clay_100_200cm_min [g/100g (%)]
- clay_100_200cm_max [g/100g (%)]
- clay_100_200cm_q05 [g/100g (%)]
- clay_100_200cm_q50 [g/100g (%)]
- clay_100_200cm_q95 [g/100g (%)]
- clay_100_200cm_stdev [g/100g (%)]

**Proportion of sand particles (> 0.05 mm) in the fine earth fraction (sand)**:
- sand_0_30cm_mean [g/100g (%)]
- sand_0_30cm_min [g/100g (%)]
- sand_0_30cm_max [g/100g (%)]
- sand_0_30cm_q05 [g/100g (%)]
- sand_0_30cm_q50 [g/100g (%)]
- sand_0_30cm_q95 [g/100g (%)]
- sand_0_30cm_stdev [g/100g (%)]
- sand_30_100cm_mean [g/100g (%)]
- sand_30_100cm_min [g/100g (%)]
- sand_30_100cm_max [g/100g (%)]
- sand_30_100cm_q05 [g/100g (%)]
- sand_30_100cm_q50 [g/100g (%)]
- sand_30_100cm_q95 [g/100g (%)]
- sand_30_100cm_stdev [g/100g (%)]
- sand_100_200cm_mean [g/100g (%)]
- sand_100_200cm_min [g/100g (%)]
- sand_100_200cm_max [g/100g (%)]
- sand_100_200cm_q05 [g/100g (%)]
- sand_100_200cm_q50 [g/100g (%)]
- sand_100_200cm_q95 [g/100g (%)]
- sand_100_200cm_stdev [g/100g (%)]

**Proportion of silt particles (≥ 0.002 mm and ≤ 0.05 mm) in the fine earth fraction (silt)**:
- silt_0_30cm_mean [g/100g (%)]
- silt_0_30cm_min [g/100g (%)]
- silt_0_30cm_max [g/100g (%)]
- silt_0_30cm_q05 [g/100g (%)]
- silt_0_30cm_q50 [g/100g (%)]
- silt_0_30cm_q95 [g/100g (%)]
- silt_0_30cm_stdev [g/100g (%)]
- silt_30_100cm_mean [g/100g (%)]
- silt_30_100cm_min [g/100g (%)]
- silt_30_100cm_max [g/100g (%)]
- silt_30_100cm_q05 [g/100g (%)]
- silt_30_100cm_q50 [g/100g (%)]
- silt_30_100cm_q95 [g/100g (%)]
- silt_30_100cm_stdev [g/100g (%)]
- silt_100_200cm_mean [g/100g (%)]
- silt_100_200cm_min [g/100g (%)]
- silt_100_200cm_max [g/100g (%)]
- silt_100_200cm_q05 [g/100g (%)]
- silt_100_200cm_q50 [g/100g (%)]
- silt_100_200cm_q95 [g/100g (%)]
- silt_100_200cm_stdev [g/100g (%)]

**Soil organic carbon content in the fine earth fraction (soil_organic_carbon)**:
- soil_organic_carbon_0_30cm_mean [g/kg]
- soil_organic_carbon_0_30cm_min [g/kg]
- soil_organic_carbon_0_30cm_max [g/kg]
- soil_organic_carbon_0_30cm_q05 [g/kg]
- soil_organic_carbon_0_30cm_q50 [g/kg]
- soil_organic_carbon_0_30cm_q95 [g/kg]
- soil_organic_carbon_0_30cm_stdev [g/kg]
- soil_organic_carbon_30_100cm_mean [g/kg]
- soil_organic_carbon_30_100cm_min [g/kg]
- soil_organic_carbon_30_100cm_max [g/kg]
- soil_organic_carbon_30_100cm_q05 [g/kg]
- soil_organic_carbon_30_100cm_q50 [g/kg]
- soil_organic_carbon_30_100cm_q95 [g/kg]
- soil_organic_carbon_30_100cm_stdev [g/kg]
- soil_organic_carbon_100_200cm_mean [g/kg]
- soil_organic_carbon_100_200cm_min [g/kg]
- soil_organic_carbon_100_200cm_max [g/kg]
- soil_organic_carbon_100_200cm_q05 [g/kg]
- soil_organic_carbon_100_200cm_q50 [g/kg]
- soil_organic_carbon_100_200cm_q95 [g/kg]
- soil_organic_carbon_100_200cm_stdev [g/kg]
