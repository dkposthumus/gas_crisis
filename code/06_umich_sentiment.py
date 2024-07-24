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

umich_comp_consumers_df = pd.read_csv(f'{raw_data}/umich_comp_cons.csv', header=1)
umich_gas_1yr_df = pd.read_csv(f'{raw_data}/umich_gas_1yr.csv', header=1)
umich_gas_5yr_df = pd.read_csv(f'{raw_data}/umich_gas_5yr.csv', header=1)

# let's first rename our variables to have descriptive names
umich_gas_1yr_df.rename(
    columns={
        'Month': 'month',
        'Year': 'year',
    }, 
    inplace=True
)