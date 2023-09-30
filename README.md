# Ambulance Demand Forecast

Forecasting ambulance demand is critical for efficient allocation of resources and timely response to emergencies. This repository houses the data processing and modeling scripts used to forecast the demand for ambulances based on historical data, weather conditions, and public holidays.

## Project Structure

![image](https://github.com/jjoonnees/Ambulance-Demand-Forecast/assets/91951551/e6668711-91f5-4e88-8b5b-60189371f16a)


### data:
raw: Contains the raw data files, such as ambulance call logs, weather reports, and public holiday lists.

processed: Houses processed and cleaned datasets, ready for modeling.
### scripts:
Contains various scripts responsible for data preprocessing, feature generation, and model building.
### models:
Location where trained models are saved for later use.
## notebooks:
Repository of Jupyter notebooks designed for data exploration, early experimentations, and model evaluations.

## Setup
Ensure you have Python 3.10 installed.
Navigate to the project directory: 

    cd Ambulance-Demand-Forecast
Install the necessary libraries: 

    pip install -r requirements.txt


## Workflow
### 1. Data Processing
Run the data_processing.py script to preprocess the raw data. This includes:

Merging and grouping ambulance data by the hour.

Generating public holiday data.

Processing weather data and merging it with the ambulance dataset.

Calculating rolling counts for historical ambulance demand.


'python scripts/data_processing.py'

### 2. Model Building
Execute the model_building.py script to train forecasting models on the processed data. Models included:

Deep Learning model using TensorFlow.

XGBoost regression model.

TensorFlow Decision Forests regression model.


    python scripts/model_building.py

## Evaluation
Models undergo evaluation using metrics like MSE, MAE, and R^2 on test data. Dive into the notebooks directory for detailed evaluations and visualizations.

## Google Colab Execution
For GPU-intensive training, utilize the provided Jupyter notebooks on Google Colab. Instructions are detailed in the Configuration Manual.
