### ***IMPORTANT**
### This script has not been tested localy due to GPU limitations
## Run ''notebooks\Ambulance_demand_time_series_Final_Models.ipynb'' from this directory on Colab

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau
from tensorflow.keras import regularizers
import xgboost as xgb
from sklearn.model_selection import GridSearchCV
import tensorflow_decision_forests as tfdf

# Defining paths for the datasets

processed_path = 'C:\\Users\\CiaranJones\\Documents\\GitHub\\Ambulance-Demand-Forecast\\data\\processed'
raw_path = 'C:\\Users\\CiaranJones\\Documents\\GitHub\\Ambulance-Demand-Forecast\\data\\raw'

# Load and preprocess data
def load_data():
    df = pd.read_csv(os.path.join(processed_path, "Final_full_ambulance_df.csv"))
    df['Date'] = pd.to_datetime(df['Date'])
    df = df.sort_values('Date')
    df['Year'] = df['Date'].dt.year
    return df

# Train the deep learning model
def train_dl_model(train_features, train_target, valid_features, valid_target):
    model = Sequential([
        Dense(32, input_dim=train_features.shape[1], activation='relu', kernel_regularizer=regularizers.l2(0.01)),
        Dropout(0.2),
        Dense(16, activation='relu', kernel_regularizer=regularizers.l2(0.01)),
        Dropout(0.2),
        Dense(1)
    ])
    model.compile(loss='mae', optimizer=Adam())
    early_stopping = EarlyStopping(monitor='val_loss', patience=10)
    lr_scheduler = ReduceLROnPlateau(monitor='val_loss', factor=0.2, patience=5, min_lr=0.001)

    model.fit(train_features, train_target, validation_data=(valid_features, valid_target), epochs=50, batch_size=256, callbacks=[early_stopping, lr_scheduler])
    model.save(os.path.join(MODEL_PATH, "dl_model.h5"))
    return model

# Train the XGBoost model
def train_xgb_model(train_features, train_target):
    params = {
        'max_depth': [4, 6, 8],
        'min_child_weight': [1, 3, 5],
        'eta': [0.1, 0.3, 0.5],
        'subsample': [0.8, 1.0],
        'colsample_bytree': [0.8, 1.0],
        'objective': ['reg:squarederror']
    }
    grid_search = GridSearchCV(estimator=xgb.XGBRegressor(), param_grid=params, scoring='neg_mean_squared_error', cv=5)
    grid_search.fit(train_features, train_target)
    best_model = xgb.XGBRegressor(**grid_search.best_params_)
    best_model.save(os.path.join(MODEL_PATH, "xgb_model.pkl"))
    return best_model

# Train the TF Decision Forests model
def train_tfdf_model(train_dataset, valid_dataset):
    model = tfdf.keras.RandomForestModel(task=tfdf.keras.Task.REGRESSION)
    model.compile(metrics=["mse"])
    model.fit(train_dataset, validation_data=valid_dataset)
    model.save(os.path.join(MODEL_PATH, "tfdf_model"))
    return model

def main():
    df = load_data()

    # Preprocess for Deep Learning and XGBoost
    df2 = df[["Unnamed: 0", 'Count for this hour in last 7 days', 'Count for this hour in last 14 days', 'Count for this hour in last 28 days', 'weekend', 'Date', 'Time Of Call', 'Count', 'Station Area', 'Public Holiday']]
    data = df2.copy()
    data["Count"] = np.log1p(data["Count"])
    data = pd.get_dummies(data, columns=["Station Area"])
    features = data.drop(columns=["Count", "Date", "Unnamed: 0"])
    target = data["Count"]
    train_size = int(len(data) * 0.7)
    valid_size = int(len(data) * 0.2)
    train_features, valid_features, test_features = features[:train_size], features[train_size:train_size + valid_size], features[train_size + valid_size:]
    train_target, valid_target, test_target = target[:train_size], target[train_size:train_size + valid_size], target[train_size + valid_size:]
    scaler = StandardScaler()
    train_features, valid_features, test_features = scaler.fit_transform(train_features), scaler.transform(valid_features), scaler.transform(test_features)

    dl_model = train_dl_model(train_features, train_target, valid_features, valid_target)
    
    xgb_model = train_xgb_model(train_features, train_target)
    
    # Preprocess for TF Decision Forests
    df1 = df[["Unnamed: 0", 'Station Area', 'Date', 'Time Of Call', 'Count', 'day_of_week', 'month', 'weekend', 'season']]
    data = df1.copy()
    data["Count"] = np.log1p(data["Count"])
    le = LabelEncoder()
    data["Station Area"] = le.fit_transform(data["Station Area"])
    features = data.drop(columns=["Count", "Date    , "Unnamed: 0"])
    target = data["Count"]
    train_size = int(len(data) * 0.7)
    valid_size = int(len(data) * 0.2)
    
    train_dataset = tfdf.keras.pd_dataframe_to_tf_dataset(data[:train_size], task=tfdf.keras.Task.REGRESSION)
    valid_dataset = tfdf.keras.pd_dataframe_to_tf_dataset(data[train_size:train_size + valid_size], task=tfdf.keras.Task.REGRESSION)

    tfdf_model = train_tfdf_model(train_dataset, valid_dataset)
    
    # Prediction & Evaluation for all models
    dl_preds = dl_model.predict(test_features)
    xgb_preds = xgb_model.predict(test_features)
    tfdf_preds = tfdf_model.predict(tfdf.keras.pd_dataframe_to_tf_dataset(data[train_size + valid_size:], task=tfdf.keras.Task.REGRESSION))

    for preds, model_name in zip([dl_preds, xgb_preds, tfdf_preds], ["Deep Learning", "XGBoost", "TF Decision Forests"]):
        mse = mean_squared_error(test_target, preds)
        mae = mean_absolute_error(test_target, preds)
        r2 = r2_score(test_target, preds)
        print(f"{model_name} Results:")
        print(f"MSE: {mse}")
        print(f"MAE: {mae}")
        print(f"R2 Score: {r2}\n")

if __name__ == "__main__":
    main()
