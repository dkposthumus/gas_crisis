import requests
import json
import pandas as pd
from pathlib import Path
import statsmodels.api as sm
import numpy as np
import matplotlib.pyplot as plt
# let's create a set of locals referring to our directory and working directory 
home_dir = Path.home()
work_dir = (home_dir / 'gas_crisis')
data = (work_dir / 'data')
raw_data = (data / 'raw')
code = Path.cwd() 
output = (work_dir / 'output')

master_df = pd.read_csv(f'{data}/master.csv')
master_df['date']= pd.to_datetime(master_df['date'])
master_df.set_index('date', inplace=True)

# first, keep only observations after June 01, 1983
cutoff_date = pd.to_datetime('1983-06-01')
filtered_df = master_df[master_df.index > cutoff_date] 

# First i need to regress daily Brent oil price percent change on daily changes in S&P500, read broad dollar, and 10-year treasury
X = master_df[['sp 500 daily chg', '10 yr yield daily chg', 'nominal broad dollar daily chg']]
y = master_df['brent price (nominal) daily pct chg']
model = sm.OLS(y, X, missing='drop').fit()
print(model.summary())
# now generate residuals
residuals = model.resid
master_df['residuals'] = residuals

master_df.rename(
    columns={
        bloomberg_df.columns[0]: 'date',
        'meeting': 'Meeting',
        'no decision': 'No-Decision Meeting',
        'production cut': 'Production Cut', 
        'production rise': 'Production Increase', 
        'production decision': 'Decision Announcement',
    }, 
    inplace=True
)

opec_var = [
    'Meeting', 'No-Decision Meeting', 
    'Production Cut', 'Production Increase', 'Decision Announcement',
]
for var in opec_var:
# now i need to create dummies for the following days: 
    # -4, -3, -2, -1, 0, 1, 2, 3, 4 days since an OPEC announcement of production cut
    days_before_after = [-4, -3, -2, -1, 1, 2, 3, 4]
    for day in days_before_after:
        col_name = f'{var}_{abs(day)}_{"before" if day < 0 else "after"}'
        master_df[col_name] = 0

    # Set the dummy variables based on row positions
    for i in range(len(master_df)):
        if master_df[var].iloc[i] == 1:
            for day in days_before_after:
                target_row = i + day
                if 0 <= target_row < len(master_df):
                    col_name = f'{var}_{abs(day)}_{"before" if day < 0 else "after"}'
                    master_df.iloc[target_row, master_df.columns.get_loc(col_name)] = 1

    # now regress the residaul on a constant and indicators for each of the date dummies
    X = master_df[[f'{var}_4_before', f'{var}_3_before', f'{var}_2_before',
                                  f'{var}_1_before', f'{var}', f'{var}_1_after',
                                  f'{var}_2_after', f'{var}_3_after', f'{var}_4_after']]
    y = master_df['residuals']
    X = sm.add_constant(X)

    model = sm.OLS(y, X, missing='drop').fit()
    print(model.summary())

    # now plot
    coefficients = model.params
    conf_int = model.conf_int(alpha=0.05)

    # Create a DataFrame for coefficients and their confidence intervals
    coefficients_df = pd.DataFrame({
        'Coefficient': coefficients,
        'Lower CI': conf_int[0],
        'Upper CI': conf_int[1]
    })

    # Filter for the dummy variables only (excluding the constant term)
    dummies_df = coefficients_df.loc[[f'{var}_4_before', f'{var}_3_before', f'{var}_2_before',
                                  f'{var}_1_before', f'{var}', f'{var}_1_after',
                                  f'{var}_2_after', f'{var}_3_after', f'{var}_4_after']]

    # Plot the coefficients with confidence intervals
    plt.figure(figsize=(14, 7))
    plt.plot(dummies_df.index, dummies_df['Coefficient'], marker='o', linestyle='-', label='Coefficient')
    plt.fill_between(dummies_df.index, dummies_df['Lower CI'], dummies_df['Upper CI'], color='b', alpha=0.2, label='95% CI')
    plt.axhline(0, color='black', linewidth=1.5, linestyle='--')
    plt.axvline(f'{var}', color='black', linewidth=2, linestyle='--', label=f'{var}')
    plt.title(f'Impact of {var} on Absolute Value of Oil Price Moves')
    plt.xlabel('Time Dummies')
    plt.ylabel('Coefficient Value')
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.legend()
    plt.savefig(f'{output}/{var}_effect_plot.png')
    plt.show()