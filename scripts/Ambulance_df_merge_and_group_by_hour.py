import pandas as pd
import os

processed_path = 'C:\\Users\\CiaranJones\\Documents\\GitHub\\Ambulance-Demand-Forecast\\data\\processed'
raw_path = 'C:\\Users\\CiaranJones\\Documents\\GitHub\\Ambulance-Demand-Forecast\\data\\raw'

def load_dataframes():
    df1 = pd.read_csv(os.path.join(raw_path, '2013-2015-dfb-ambulance (1).csv'))
    df2 = pd.read_csv(os.path.join(raw_path, 'dccfirebrigadeambulanceincidents2012.csv'))
    df3 = pd.read_csv(os.path.join(raw_path, 'da-opendata-2016-to-2017-with-stn-area.csv'))
    df4 = pd.read_csv(os.path.join(raw_path, 'da-opendata-2018-to-2019-with-stn-area.csv'))
    df5 = pd.read_csv(os.path.join(raw_path, 'da-opendata-2020-to-2022-with-stn-area.csv'))
    return df1, df2, df3, df4, df5

def process_dataframes(df1, df2, df3, df4, df5):
    df2 = df2.rename(columns={'Description': 'Clinical Status'})
    df = pd.concat([df2, df1], ignore_index=True)
    
    clinical_status_map = {
        'A': 'Alpha', 'B': 'Bravo', 'BRAVO': 'Bravo', 'C': 'Charlie', 'D': 'Delta',
        'E': 'Echo', 'O': 'Omega', '999/112 Incident Non ProQa': 'Not Classed',
        'Non ProQa Class': 'Not Classed'
    }
    df['Clinical Status'] = df['Clinical Status'].replace(clinical_status_map)
    
    df3 = pd.concat([df3, df4, df5], ignore_index=True)
    df3['Station Name'] = df3['Station Name'].str.replace(' Fire Station', '')
    df3 = df3[~df3['Station Name'].str.contains('Null')]
    df3.dropna(subset=['Station Name'], inplace=True)
    df3.rename(columns={'Station Name': 'Station Area', 'criticality': 'Clinical Status'}, inplace=True)
    df3['Time Of Call'] = pd.to_datetime(df3['TOC']).dt.hour
    df3['Date'] = pd.to_datetime(df3['Date'], dayfirst=True)
    df3['Clinical Status'] = df3['Clinical Status'].replace(clinical_status_map)
    df3.drop('ID', axis=1, inplace=True)
    
    df['TOC'] = pd.to_datetime(df['TOC'])
    df['Time Of Call'] = df['TOC'].dt.strftime('%H')
    df_concat = pd.concat([df, df3], ignore_index=True)
    df_concat = df_concat[~df_concat['Date'].astype(str).str.contains('2012')]
    
    df_new = df_concat.loc[:, ['Date', 'Station Area', 'Clinical Status', 'Time Of Call']]
    df_new['Date'] = pd.to_datetime(df_new['Date'])
    df_new['Date'] = df_new['Date'].dt.date
    
    df_grouped = df_new.groupby(['Date', 'Station Area', 'Time Of Call']).size().reset_index(name='Count')
    df_grouped['Station Area'].replace({'Tara Street': 'Tara St', 'Phibsboro': 'Phibsborough'}, inplace=True)
    
    df_grouped['Date'] = pd.to_datetime(df_grouped['Date'], format='%Y-%m-%d').dt.date.astype(str)
    df_grouped['Date'] = pd.to_datetime(df_grouped['Date'], format='%Y-%m-%d')
    df_grouped['Time Of Call'] = df_grouped['Time Of Call'].astype(int)
    
    station_areas = df_grouped['Station Area'].unique()
    dates = df_grouped['Date'].unique()
    times = [str(i).zfill(2) for i in range(24)]
    index = pd.MultiIndex.from_product([station_areas, dates, times], names=['Station Area', 'Date', 'Time Of Call'])
    empty_df = pd.DataFrame(index=index).reset_index()
    empty_df['Date'] = pd.to_datetime(empty_df['Date'], format='%Y-%m-%d')
    empty_df['Time Of Call'] = empty_df['Time Of Call'].astype(int)
    
    merged_df = pd.merge(empty_df, df_grouped, how='left', on=['Station Area', 'Date', 'Time Of Call'])
    merged_df['Count'] = merged_df['Count'].fillna(0)
    merged_df['Date'] = pd.to_datetime(merged_df['Date'])
    
    yearly_count = merged_df.groupby(pd.Grouper(key='Date', freq='Y'))['Count'].sum().reset_index()
    yearly_count = yearly_count.rename(columns={'Date': 'Year'})
    
    merged_df.to_csv(os.path.join(processed_path, 'ambulance_calls_hourly_2012_to_2022.csv'), index=False)

def main():
    df1, df2, df3, df4, df5 = load_dataframes()
    process_dataframes(df1, df2, df3, df4, df5)

if __name__ == "__main__":
    main()
