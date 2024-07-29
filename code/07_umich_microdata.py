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

umich_microdata_df = pd.read_csv(f'{raw_data}/umich_microdata.csv', header=0)



umich_microdata_df.to_csv(f'{data}/umich_microdata.csv', index=False)

