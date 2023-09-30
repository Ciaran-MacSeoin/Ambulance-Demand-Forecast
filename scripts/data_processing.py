from Ambulance_df_merge_and_group_by_hour import main as merge_and_group
from Public_holidays_df_generator import generate_and_save_holidays
from Rolling_counts_calculation import main as rolling_counts_main
from Weather_Dublin_and_merge import main as process_weather_data
import os


def execute_all_scripts():
    print("Merging and Grouping Ambulance Data...")
    merge_and_group()

    print("Generating Public Holidays Data...")
    generate_and_save_holidays()

    print("Processing Weather Data and Merging...")
    process_weather_data()

    print("Calculating Rolling Counts...")
    rolling_counts_main()

if __name__ == "__main__":
    execute_all_scripts()