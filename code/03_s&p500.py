import requests
import json
import pandas as pd
from pathlib import Path
from fredapi import Fred
# let's create a set of locals referring to our directory and working directory 
home_dir = Path.home()
work_dir = (home_dir / 'gas_crisis')
data = (work_dir / 'data')
raw_data = (data / 'raw')
code = Path.cwd() 
# first, let's use an API to pull current data on the S&P500 index
    # unfortunately, FRED only has S&P500 data back to 2014, so I'm only pulling index
    # values starting currently and then appending to a historical dataframe
fred = Fred(api_key='8905b2f5faefd705486e644f09bb8088')
sp500_fred = fred.get_series('SP500')
sp500_fred_df = sp500_fred.reset_index()
sp500_fred_df.columns = ['date', 's&p 500']
# now filter so that observations start on july 24, 2024
sp500_fred_df['date'] = pd.to_datetime(sp500_fred_df['date'])
start_date = pd.to_datetime('2024-07-24')
sp500_fred_df = sp500_fred_df[sp500_fred_df['date'] >= start_date]
# now let's import the necessary excel file
sp500_historical_df = pd.read_csv(f'{raw_data}/s&p_historical.csv', header=0)
# keep only the close value, since that's what is reported
cols_keep = ['Date', ' Close']
sp500_historical_df = sp500_historical_df[cols_keep]
sp500_historical_df.rename(
    columns={
        'Date': 'date',
        ' Close': 's&p 500'
    }, 
    inplace=True
)
sp500_df = pd.concat([sp500_fred_df, sp500_historical_df], axis=0, ignore_index=True)
sp500_df['date'] = pd.to_datetime(sp500_df['date'])
sp500_df.to_csv(f'{data}/sp500.csv', index=False)