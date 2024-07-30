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

# these are hard coded from the goldman opec article in the resources folder of this github
    # see exhibit 1 on page 2
dates = [
    'Mar 30 1998', 'Jun 24 1998', 'Nov 26 1998', 'Mar 23 1999', 'Mar 29 2000', 
    'Mar 17 2001', 'Dec 12 2002', 'Sep 24 2003', 'Feb 10 2004', 'Dec 10 2004', 
    'Sep 11 2006', 'Dec 14 2006', 'Oct 24 2008', 'Dec 17 2008', 'Sep 28 2016', 
    'Nov 30 2016', 'Dec 7 2018', 'Dec 6 2019', 'Mar 5 2020', 'Apr 9 2020', 
    'Oct 5 2022'
]
goldman_opec_df = pd.DataFrame({'date': dates})
goldman_opec_df['date'] = pd.to_datetime(goldman_opec_df['date'])
# generate a dummy variable which is equal to 1 for all these dates
goldman_opec_df['production cut'] = 1

goldman_opec_df.to_csv(f'{data}/goldman_opec.csv', index=False)