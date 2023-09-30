import os
from Ambulance_demand_time_series_Final_Models import main as model_building_main


def execute_all_scripts():

    print("Building Models...")
    model_building_main()

if __name__ == "__main__":
    execute_all_scripts()