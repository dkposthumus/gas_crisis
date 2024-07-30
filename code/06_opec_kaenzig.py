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

# this is taken from a paper written by kaenzig
kaenzig_df = pd.read_csv(f'{raw_data}/opec_kaenzig.csv', header=1)
# drop the 'Announcement' and 'Notes'
kaenzig_df = kaenzig_df.drop(columns=['Announcement day', 'Notes', 'Meeting classification: Ordinary (1), Extraordinary (2), Other (3)'])
# now let's generate a few different types of dummies:
kaenzig_df['meeting'] = 1
kaenzig_df['no decision'] = np.where(kaenzig_df['Decision'] == 0, 1, 0)
kaenzig_df['production cut'] = np.where(kaenzig_df['Decision'] == -1, 1, 0)
kaenzig_df['production rise'] = np.where(kaenzig_df['Decision'] == 1, 1, 0)
kaenzig_df['production decision'] = np.where(kaenzig_df['Decision'] != 0, 1, 0)

kaenzig_df.rename(
    columns={
        'Trading day': 'date',
    }, 
    inplace=True
)

kaenzig_df['date'] = pd.to_datetime(kaenzig_df['date'])

kaenzig_df.to_csv(f'{data}/opec_kaenzig.csv', index=False)