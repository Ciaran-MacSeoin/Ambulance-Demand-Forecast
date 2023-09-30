import pandas as pd
import os

# Paths
RAW_PATH = 'C:\\Users\\CiaranJones\\Documents\\GitHub\\Ambulance-Demand-Forecast\\data\\raw'
PROCESSED_PATH = 'C:\\Users\\CiaranJones\\Documents\\GitHub\\Ambulance-Demand-Forecast\\data\\processed'

def load_weather_data():
    df = pd.read_csv(os.path.join(RAW_PATH, 'hly532 -2.csv'))
    df['date'] = pd.to_datetime(df['date'])
    df = df[(df['date'] >= '2012-01-01') & (df['date'] <= '2023-01-01')]
    df['hour'] = df['date'].dt.strftime('%H')
    df['date_only'] = pd.to_datetime(df['date'].dt.date)

    cols_to_keep = [col for col in df.columns if 'ind' not in col]
    df = df[cols_to_keep]

    float_cols = df.select_dtypes(include=['float']).columns
    df[float_cols] = df[float_cols].astype('object')

    return df

def load_ambulance_data():
    df = pd.read_csv(os.path.join(PROCESSED_PATH, 'ambulance_calls_hourly_2012_to_2022.csv'))
    df['Date'] = pd.to_datetime(df['Date'])
    df['datetime'] = pd.to_datetime(df['Date'].astype(str) + ' ' + df['Time Of Call'].astype(str).str.zfill(2) + ':00:00')
    
    return df

def calculate_yearly_count(df):
    yearly_count = df.groupby(pd.Grouper(key='Date', freq='Y'))['Count'].sum().reset_index()
    yearly_count = yearly_count.rename(columns={'Date': 'Year'})
    print(yearly_count)

def merge_data(ambulance_df, weather_df):
    ambulance_df['datetime'] = pd.to_datetime(ambulance_df['Date'].astype(str) + ' ' + ambulance_df['Time Of Call'].astype(str).str.zfill(2) + ':00:00')
    merged_df = pd.merge(ambulance_df, weather_df, left_on='datetime', right_on='date')
    merged_df.drop(['datetime'], axis=1, inplace=True)
    
    merged_df['Count'] = merged_df['Count'].astype(int)
    merged_df['day_of_week'] = merged_df['date'].dt.dayofweek
    merged_df['month'] = merged_df['date'].dt.month
    merged_df['weekend'] = (merged_df['date'].dt.dayofweek >= 5).astype(int)
    merged_df['season'] = ((merged_df['month'] % 12 + 3) // 3).astype(int)

    return merged_df

def incorporate_public_holidays(merged_df):
    pub_holiday_df = pd.read_csv(os.path.join(PROCESSED_PATH, 'public_holiday_df_2012_2023.csv'))
    pub_holiday_df['Date'] = pd.to_datetime(pub_holiday_df['Date'])
    merged_with_holidays = pd.merge(merged_df, pub_holiday_df, on="Date")
    
    return merged_with_holidays

def save_to_csv(df, filename):
    df.to_csv(os.path.join(PROCESSED_PATH, filename), index=False)

def main():
    weather_df = load_weather_data()
    ambulance_df = load_ambulance_data()
    
    save_to_csv(weather_df, 'dublin_weather_2012-2022.csv')
    
    calculate_yearly_count(ambulance_df)
    merged_df = merge_data(ambulance_df, weather_df)
    final_df = incorporate_public_holidays(merged_df)
    save_to_csv(final_df, 'calls_weather_pubhols_25_04_2023.csv')

if __name__ == "__main__":
    main()
