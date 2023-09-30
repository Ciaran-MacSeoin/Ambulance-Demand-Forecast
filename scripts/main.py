import os
from Ambulance demand time series Final Models import main as model_building_main
from Ambulance_df_merge_and_group_by_hour import main as merge_and_group
from Public holidays df generator import generate_and_save_holidays
from Rolling counts calculation import main as rolling_counts_main
from Weather-Dublin_and merge import process_weather_data

DATA_DIR = os.path.join("C:", "Users", "CiaranJones", "Documents", "GitHub", "Ambulance-Demand-Forecast", "data", "processed")
SCRIPTS_DIR = os.path.join("C:", "Users", "CiaranJones", "Documents", "GitHub", "Ambulance-Demand-Forecast", "scripts")

def execute_all_scripts():
    print("Merging and Grouping Ambulance Data...")
    merge_and_group(DATA_DIR)

    print("Generating Public Holidays Data...")
    generate_and_save_holidays(DATA_DIR)

    print("Processing Weather Data and Merging...")
    process_weather_data(DATA_DIR)

    print("Calculating Rolling Counts...")
    rolling_counts_main(DATA_DIR)

    print("Building Models...")
    model_building_main()

if __name__ == "__main__":
    execute_all_scripts()