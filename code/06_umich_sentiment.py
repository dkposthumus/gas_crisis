import requests
import json
import pandas as pd
from pathlib import Path
# import matplotlib.pyplot as plt
# let's create a set of locals referring to our directory and working directory 
home_dir = Path.home()
work_dir = (home_dir / 'gas_crisis')
data = (work_dir / 'data')
raw_data = (data / 'raw')
code = Path.cwd() 

umich_df = pd.read_csv(f'{raw_data}/umich_raw_all_tables.csv', header=1)

# let's do a mass renaming of variables according to the time series codebook (found in the 'resources' folder)
umich_df['day'] = 1
# Create a 'date' string column by concatenating 'year', 'month', and 'day'
umich_df['date_str'] = umich_df['yyyy'].astype(str) + '-' + umich_df['Month'].astype(str) + '-' + umich_df['day'].astype(str)
# Convert the 'date_str' column to a datetime coumn
umich_df['date'] = pd.to_datetime(umich_df['date_str'], format='%Y-%m-%d')

umich_df.rename(
    columns={
        'ics_all': 'consumer sentiment index (ics)',
        'ics_inc31': 'ics, bottom 1/3 income',
        'ics_inc32': 'ics, middle 1/3 income',
        'ics_inc33': 'ics, top 1/3 income',
        'ics_a1834': 'ics, 18-34 age',
        'ics_a3554': 'ics, 35-54 age',
        'ics_a5597': 'ics, 55+ age',
        'icc_all': 'index of current econ conditions (icc)',
        'ice_all': 'index of consumer expectations (ice)',
        'pexp_r_all': 'personal 1yr expectation',
        'ptrd_r_all': '1yr personal trend',
        'pexp5_r_all': 'personal 5yr expectation',
        'ptrd5_r_all': '5yr personal trend',
        'inex_med_all': 'median expected 1yr income change',
        'rinc_r_all': '1yr inflation/income expectation',
        'pssa_mean_all': 'chances social security is adequate to maintain living standards',
        'news_r_all': 'favorability of news re: business conditions',
        'bago_r_all': '1yr change in business conditions',
        'bexp_r_all': 'business 1yr expectations',
        'btrd_r_all': '1yr business trend',
        'bus5_r_all': 'economic 5yr expectations',
        'umex_r_all': 'unemployment 1yr expectations',
        'ratex_r_all': 'interest rate 1yr expectations',
        'px1_mean_all': '1yr mean inflation expectations',
        'px1_med_all': '1yr median inflation expectations',
        'px5_mean_all': '5-10yr mean inflation expectations',
        'px5_med_all': '5-10yr median inflation expectations',
        'govt_r_all': 'govt good/bad policy fighting inflation',
        'veh_r_all': 'good/bad time to buy vehicle',
        'gas1px_md_all': '1yr median gas price change expectation',
        'gas1px_mean_all': '1yr mean gas price change expectation',
        'hom_r_all': 'good/bad time to buy house',
        'shom_r_all': 'good/bad time to sell house',
    },
    inplace=True
)

# now specify columns: 
cols_keep=[
    'date', 'consumer sentiment index (ics)', 'ics, bottom 1/3 income', 'ics, middle 1/3 income',
    'ics, top 1/3 income', 'ics, 18-34 age', 'ics, 35-54 age', 'ics, 55+ age', 'index of current econ conditions (icc)',
    'index of consumer expectations (ice)', 'personal 1yr expectation', '1yr personal trend', 'personal 5yr expectation',
    '5yr personal trend', 'median expected 1yr income change', '1yr inflation/income expectation',
    'chances social security is adequate to maintain living standards',
    'favorability of news re: business conditions', '1yr change in business conditions',
    'business 1yr expectations', '1yr business trend', 'economic 5yr expectations',
    'unemployment 1yr expectations', 'interest rate 1yr expectations', '1yr mean inflation expectations',
    '1yr median inflation expectations', '5-10yr mean inflation expectations',
    '5-10yr median inflation expectations', 'govt good/bad policy fighting inflation',
    'good/bad time to buy vehicle', '1yr median gas price change expectation',
    '1yr mean gas price change expectation', 'good/bad time to buy house', 'good/bad time to sell house',
]
umich_df = umich_df[cols_keep]

umich_df.to_csv(f'{data}/umich.csv', index=False)

# let's plot 