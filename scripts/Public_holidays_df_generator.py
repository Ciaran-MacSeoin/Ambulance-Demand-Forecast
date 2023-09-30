import pandas as pd
from datetime import datetime, timedelta
import os

# Data Paths
REPO_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(REPO_DIR, "data", "processed")

# Data Preparation
HOLIDAY_DATA = [
    # Holidays and Observances in Ireland for 2012 - 2023
    # Date, Name, Type
    ("2012-01-01", "New Year's Day", "National holiday"),
    ("2012-03-17", "St. Patrick's Day", "National holiday"),
    ("2012-04-09", "Easter Monday", "National holiday"),
    ("2012-05-07", "May Day", "National holiday"),
    ("2012-06-04", "June Bank Holiday", "National holiday"),
    ("2012-08-06", "August Bank Holiday", "National holiday"),
    ("2012-10-29", "October Bank Holiday", "National holiday"),
    ("2012-12-25", "Christmas Day", "National holiday"),
    ("2012-12-26", "St. Stephen's Day", "National holiday"),
    
    #2013
    ("2013-01-01", "New Year's Day", "National holiday"),
    ("2013-03-17", "St. Patrick's Day", "National holiday"),
    ("2013-04-01", "Easter Monday", "National holiday"),
    ("2013-05-06", "May Day", "National holiday"),
    ("2013-06-03", "June Bank Holiday", "National holiday"),
    ("2013-08-05", "August Bank Holiday", "National holiday"),
    ("2013-10-28", "October Bank Holiday", "National holiday"),
    ("2013-12-25", "Christmas Day", "National holiday"),
    ("2013-12-26", "St. Stephen's Day", "National holiday"),

    # Add other holidays and observances for each year
    # 2014
    ("2014-01-01", "New Year's Day", "National holiday"),
    ("2014-03-17", "St. Patrick's Day", "National holiday"),
    ("2014-04-21", "Easter Monday", "National holiday"),
    ("2014-05-05", "May Day", "National holiday"),
    ("2014-06-02", "June Bank Holiday", "National holiday"),
    ("2014-08-04", "August Bank Holiday", "National holiday"),
    ("2014-10-27", "October Bank Holiday", "National holiday"),
    ("2014-12-25", "Christmas Day", "National holiday"),
    ("2014-12-26", "St. Stephen's Day", "National holiday"),

    # 2015
    ("2015-01-01", "New Year's Day", "National holiday"),
    ("2015-03-17", "St. Patrick's Day", "National holiday"),
    ("2015-04-06", "Easter Monday", "National holiday"),
    ("2015-05-04", "May Day", "National holiday"),
    ("2015-06-01", "June Bank Holiday", "National holiday"),
    ("2015-08-03", "August Bank Holiday", "National holiday"),
    ("2015-10-26", "October Bank Holiday", "National holiday"),
    ("2015-12-25", "Christmas Day", "National holiday"),
    ("2015-12-26", "St. Stephen's Day", "National holiday"),

    # 2016
    ("2016-01-01", "New Year's Day", "National holiday"),
    ("2016-03-17", "St. Patrick's Day", "National holiday"),
    ("2016-03-28", "Easter Monday", "National holiday"),
    ("2016-05-02", "May Day", "National holiday"),
    ("2016-06-06", "June Bank Holiday", "National holiday"),
    ("2016-08-01", "August Bank Holiday", "National holiday"),
    ("2016-10-31", "October Bank Holiday", "National holiday"),
    ("2016-12-25", "Christmas Day", "National holiday"),
    ("2016-12-26", "St. Stephen's Day", "National holiday"),

    # 2017
    ("2017-01-01", "New Year's Day", "National holiday"),
    ("2017-03-17", "St.Patrick's Day", "National holiday"),
    ("2017-04-17", "Easter Monday", "National holiday"),
    ("2017-05-01", "May Day", "National holiday"),
    ("2017-06-05", "June Bank Holiday", "National holiday"),
    ("2017-08-07", "August Bank Holiday", "National holiday"),
    ("2017-10-30", "October Bank Holiday", "National holiday"),
    ("2017-12-25", "Christmas Day", "National holiday"),
    ("2017-12-26", "St. Stephen's Day", "National holiday"),
    # 2018
    ("2018-01-01", "New Year's Day", "National holiday"),
    ("2018-03-17", "St. Patrick's Day", "National holiday"),
    ("2018-04-02", "Easter Monday", "National holiday"),
    ("2018-05-07", "May Day", "National holiday"),
    ("2018-06-04", "June Bank Holiday", "National holiday"),
    ("2018-08-06", "August Bank Holiday", "National holiday"),
    ("2018-10-29", "October Bank Holiday", "National holiday"),
    ("2018-12-25", "Christmas Day", "National holiday"),
    ("2018-12-26", "St. Stephen's Day", "National holiday"),

    # 2019
    ("2019-01-01", "New Year's Day", "National holiday"),
    ("2019-03-17", "St. Patrick's Day", "National holiday"),
    ("2019-04-22", "Easter Monday", "National holiday"),
    ("2019-05-06", "May Day", "National holiday"),
    ("2019-06-03", "June Bank Holiday", "National holiday"),
    ("2019-08-05", "August Bank Holiday", "National holiday"),
    ("2019-10-28", "October Bank Holiday", "National holiday"),
    ("2019-12-25", "Christmas Day", "National holiday"),
    ("2019-12-26", "St. Stephen's Day", "National holiday"),

    # 2020
    ("2020-01-01", "New Year's Day", "National holiday"),
    ("2020-03-17", "St. Patrick's Day", "National holiday"),
    ("2020-04-13", "Easter Monday", "National holiday"),
    ("2020-05-04", "May Day", "National holiday"),
    ("2020-06-01", "June Bank Holiday", "National holiday"),
    ("2020-08-03", "August Bank Holiday", "National holiday"),
    ("2020-10-26", "October Bank Holiday", "National holiday"),
    ("2020-12-25", "Christmas Day", "National holiday"),
    ("2020-12-26", "St. Stephen's Day", "National holiday"),

    # 2021
    ("2021-01-01", "New Year's Day", "National holiday"),
    ("2021-03-17", "St. Patrick's Day", "National holiday"),
    ("2021-04-05", "Easter Monday", "National holiday"),
    ("2021-05-03", "May Day", "National holiday"),
    ("2021-06-07", "June Bank Holiday", "National holiday"),
    ("2021-08-02", "August Bank Holiday", "National holiday"),
    ("2021-10-25", "October Bank Holiday", "National holiday"),
    ("2021-12-25", "Christmas Day", "National holiday"),
    ("2021-12-26", "St. Stephen's Day", "National holiday"),
    # 2022
    ("2022-01-01", "New Year's Day", "National holiday"),
    ("2022-03-17", "St. Patrick's Day", "National holiday"),
    ("2022-04-18", "Easter Monday", "National holiday"),
    ("2022-05-02", "May Day", "National holiday"),
    ("2022-06-06", "June Bank Holiday", "National holiday"),
    ("2022-08-01", "August Bank Holiday", "National holiday"),
    ("2022-10-31", "October Bank Holiday", "National holiday"),
    ("2022-12-25", "Christmas Day", "National holiday"),
    ("2022-12-26", "St. Stephen's Day", "National holiday"),

    # 2023
    ("2023-01-01", "New Year's Day", "National holiday"),
    ("2023-03-17", "St. Patrick's Day", "National holiday"),
    ("2023-04-10", "Easter Monday", "National holiday"),
    ("2023-05-01", "May Day", "National holiday"),
    ("2023-06-05", "June Bank Holiday", "National holiday"),
    ("2023-08-07", "August Bank Holiday", "National holiday"),
    ("2023-10-30", "October Bank Holiday", "National holiday"),
    ("2023-12-25", "Christmas Day", "National holiday"),
    ("2023-12-26", "St. Stephen's Day", "National holiday"),
    ]

def prepare_holiday_df(holiday_data):
    df = pd.DataFrame(holiday_data, columns=["Date", "Name", "Type"])
    df["Date"] = pd.to_datetime(df["Date"])
    return df

def is_holiday(date, holiday_data):
    holiday_row = holiday_data[holiday_data["Date"] == date]
    return 1 if not holiday_row.empty else 0

def generate_final_df(start_date, end_date, holiday_data):
    days_range = (end_date - start_date).days
    dates = [start_date + timedelta(days=i) for i in range(days_range + 1)]
    public_holidays = [is_holiday(date, holiday_data) for date in dates]
    
    df = pd.DataFrame({"Date": dates, "Public Holiday": public_holidays})
    return df

def generate_and_save_holidays():
    START_DATE = datetime(2012, 1, 1)
    END_DATE = datetime(2023, 12, 31)
    
    holiday_df = prepare_holiday_df(HOLIDAY_DATA)
    final_df = generate_final_df(START_DATE, END_DATE, holiday_df)
    
    # Save to file
    output_path = os.path.join('C:\\Users\\CiaranJones\\Documents\\GitHub\\Ambulance-Demand-Forecast\\data\\processed', 'public_holiday_df_2012_2023.csv')
    final_df.to_csv(output_path, index=False)

if __name__ == "__main__":
    generate_and_save_holidays()