import os
import pandas as pd
from glob import glob


def postprocess_isric():
    """
    Postprocess extracted ISRIC data.  

    - Aggregate and calculate a weighted average over depths:
        - 0-30 cm: 0-5 cm (5/30), 5-15 cm (10/30), 15-30 cm (15/30)
        - 30-100 cm: 30-60 cm (30/70), 60-100 cm (40/70)  
        - 100-200 cm: no aggregation needed
    - Convert to common units and rename the columns:
        | **Variable** | **Mapped unit** | **Conversation factor** | **Common unit**   | **CAMELS-DE variable name** |
        |--------------|-----------------|-------------------------|-------------------|-----------------------------|
        | bdod         | cg/cm³          | 100                     | kg/dm³            | bulk_density                |
        | cfvo         | cm3/dm3 (vol‰)  | 10                      | cm3/100cm3 (vol%) | coarse_fragments            |
        | clay         | g/kg            | 10                      | g/100g (%)        | clay                        |
        | silt         | g/kg            | 10                      | g/100g (%)        | silt                        |
        | sand         | g/kg            | 10                      | g/100g (%)        | sand                        |
        | soc          | dg/kg           | 10                      | g/kg              | soil_organic_carbon         |

    """
    # Load the data
    for variable in ["sand", "silt", "clay", "bdod", "cfvo", "soc"]:
        # Get the files
        files = glob(f"/output_data/isric_extracted/{variable}/*.csv")

        # Create dictionary over depths with the data
        data = {os.path.basename(file).split(f"{variable}_")[1].split("_")[0]: pd.read_csv(file) for file in files}

        # Create the output folder if it does not exist
        if not os.path.exists("/output_data/isric_processed"):
            os.makedirs("/output_data/isric_processed")

        # Aggregate the data
        aggregated_data = {}
        # 0-30 cm
        aggregated_data["0-30cm"] = (data["0-5cm"].iloc[:,1:] * (5 / 30) + data["5-15cm"].iloc[:,1:] * (10 / 30) + data["15-30cm"].iloc[:,1:] * (15 / 30))
        # 30-100 cm
        aggregated_data["30-100cm"] = (data["30-60cm"].iloc[:,1:] * (30 / 70) + data["60-100cm"].iloc[:,1:] * (40 / 70))
        # 100-200 cm
        aggregated_data["100-200cm"] = data["100-200cm"].iloc[:,1:]

        # Convert to common units
        if variable == "bdod":
            aggregated_data = {depth: df / 100 for depth, df in aggregated_data.items()}
        if variable in ["clay", "silt", "sand", "cfvo", "soc"]:
            aggregated_data = {depth: df / 10 for depth, df in aggregated_data.items()}

        # Add the camels_id column as the first column
        aggregated_data = {depth: pd.concat([data["0-5cm"].iloc[:,0], df], axis=1) for depth, df in aggregated_data.items()}

        # Add the depth to the column names and concatenate the dataframes
        dfs = {}
        for depth, df in aggregated_data.items():
            # Add the depth to the column names
            df.columns = [f"{depth.replace('-', '_')}_{column}" if column != "camels_id" else column for column in df.columns]
            # Save the dataframe
            dfs[depth] = df

        # Add the camels variable names to the column names
        for depth, df in dfs.items():
            if variable in ["clay", "silt", "sand"]:
                df.columns = [f"{variable}_{column}" if column != "camels_id" else column for column in df.columns]
            elif variable == "bdod":
                df.columns = [f"bulk_density_{column}" if column != "camels_id" else column for column in df.columns]
            elif variable == "cfvo":
                df.columns = [f"coarse_fragments_{column}" if column != "camels_id" else column for column in df.columns]
            elif variable == "soc":
                df.columns = [f"soil_organic_carbon_{column}" if column != "camels_id" else column for column in df.columns]

        # Concatenate the dataframes, keep only the first camels_id column
        df_result = pd.concat(dfs.values(), axis=1)
        df_result = df_result.loc[:,~df_result.columns.duplicated()]

        # Save the data
        df_result.to_csv(f"/output_data/isric_processed/{variable}_processed.csv", index=False)

        print(f"Variable: {variable} --- Postprocessing finished.")


if __name__ == "__main__":
    postprocess_isric()