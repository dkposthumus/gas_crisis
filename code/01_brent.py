import requests
import pandas as pd
import json
from pathlib import Path
# let's create a set of locals referring to our directory and working directory 
home_dir = Path.home()
work_dir = (home_dir / 'gas_crisis')
data = (work_dir / 'data')
raw_data = (data / 'raw')
code = Path.cwd() 

# I'm fetching the data using an API from EIA
# the two series I'm interested in are:
# EPCBRENT - the brent crude prices
# EIA APIS limit the number of rows per request; therefore, I'm only pulling starting on July 16, 2024
    # for the historical (i.e., pre-july 16, 2024) data, I'm pulling a spreadsheet downloaded from EIA to get around the row limit
api_url = 'https://api.eia.gov/v2/petroleum/pri/spt/data'
params = {'api_key': 'QyPbWQo92CjndZz8conFD9wb08rBkP4jnDV02TAd'}
header = {
    "frequency": "daily",
    "data": [
        "value"
    ],
    "facets": {
        "product": [
            "EPCBRENT"
        ]
    },
    "start": "2024-07-16",
    "end": "2030-01-01",
    "sort": [
        {
            "column": "period",
            "direction": "desc"
        }
    ],
    "offset": 0,
    "length": 5000
}
# now let's actually request and get the data:
brent = requests.get(
    api_url, params=params, headers={'X-Params': json.dumps(header)}
)
# Check if request was successful (if it is successful, then status code is 200)
if brent.status_code == 200:
    brent_data = brent.json()
    # Extract data from JSON structure
    brent_series = brent_data['response']['data']
    # create empty list into which I'll fill
    brent_values = []
    for data_point in brent_series:
        date = data_point['period']
        brent_price = data_point['value']
        brent_values.append(
            {
                'date': date,
                'brent price (nominal)': brent_price,
            }
        )
    # Create Pandas DataFrame
    brent_df = pd.DataFrame(brent_values)
    brent_df['date'] = pd.to_datetime(brent_df['date'])
    # Display DataFrame
    #print(brent_df)
else:
    print(f'Failed to retrieve data. Status code: {brent.status_code}')
# now, let's import the spreadsheet with the historical data
brent_historical_df = pd.read_excel(f'{raw_data}/brent_historical.xlsx', sheet_name='Data 1', header=2)
brent_historical_df.rename(
    columns={
        'Europe Brent Spot Price FOB (Dollars per Barrel)': 'brent price (nominal)',
        'Date': 'date',
    }, 
    inplace=True
)
brent_historical_df['date'] = pd.to_datetime(brent_historical_df['date'])
start_date = pd.to_datetime('2000-01-01')
brent_historical_df = brent_historical_df[brent_historical_df['date'] >= start_date]
# now append the two dataframes
brent_df = pd.concat([brent_df, brent_historical_df], axis=0, ignore_index=True)
print(brent_df)

brent_df.to_csv(f'{data}/brent_price.csv', index=False)