import os
import pandas as pd
from tqdm import tqdm

tqdm.pandas()

processed_path = 'C:\\Users\\CiaranJones\\Documents\\GitHub\\Ambulance-Demand-Forecast\\data\\processed'
raw_path = 'C:\\Users\\CiaranJones\\Documents\\GitHub\\Ambulance-Demand-Forecast\\data\\raw'

def load_data(file_name, path):
    '''Load data from the given path.'''
    return pd.read_csv(os.path.join(path, file_name))

def save_data(df, file_name, path):
    '''Save the dataframe to the given path.'''
    df.to_csv(os.path.join(path, file_name), index=False)

def main():
    df = load_data('calls_weather_pubhols_25_04_2023.csv', processed_path)
    df['date'] = pd.to_datetime(df['date'])
    df.set_index('date', inplace=True)
    
    df.sort_values(by=['Station Area', 'date'], inplace=True)

    for window, col_name in zip([1, 3, 6], ['Count_in_last_1hour', 'Count_in_last_3hours', 'Count_in_last_6hours']):
        df[col_name] = df.groupby('Station Area')['Count'].progress_apply(lambda x: x.rolling(window=f'{window}H', closed='right').sum().shift()).fillna(0)

    hourly_sums = df.groupby(['Station Area', df.index.date, df.index.hour])['Count'].sum().reset_index(name='Hourly_Count')
    hourly_sums.columns = ['Station Area', 'Date', 'Hour', 'Hourly_Count']

    for window, col_name in zip([7, 14, 28], ['Count_in_last_7days', 'Count_in_last_14days', 'Count_in_last_28days']):
        hourly_sums[col_name] = hourly_sums.groupby(['Station Area', 'Hour'])['Hourly_Count'].progress_apply(lambda x: x.rolling(window=window).sum()).fillna(0)

    df = df.merge(hourly_sums.drop(columns=['Hourly_Count']), left_on=['Station Area', df.index.date, df.index.hour], right_on=['Station Area', 'Date', 'Hour'], how='left')
    df.reset_index(inplace=True)

    for col_name in ['Count_in_last_1hour', 'Count_in_last_3hours', 'Count_in_last_6hours', 'Count_in_last_7days', 'Count_in_last_14days', 'Count_in_last_28days']:
        df[col_name] = df[col_name].astype('int')

    columns_to_keep = ['Station Area', 'Date', 'Time Of Call', 'Count', 'rain', 'temp', 'wetb', 'dewpt', 'vappr', 'rhum', 'msl', 'wdsp', 'wddir', 'ww', 'w', 'sun',
       'vis', 'clht', 'clamt', 'day_of_week', 'month', 'weekend', 'season', 'Public Holiday', 'Count_in_last_1hour', 'Count_in_last_3hours',
       'Count_in_last_6hours', 'Count_in_last_7days', 'Count_in_last_14days', 'Count_in_last_28days']

    df = df[columns_to_keep]
    save_data(df, 'Final_full_ambulance_df.csv', processed_path)

if __name__ == "__main__":
    main()
