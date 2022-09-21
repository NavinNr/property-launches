import pandas as pd
import sys

# read launch data and summarize by year
launch_df = pd.read_csv("launch_data.csv")
launch_df[['year', 'qtr']] = launch_df['quarter'].str.split('-', expand=True)
launch_df['year'] = launch_df['year'].astype(str).astype(int)
launch_df_sum = launch_df.groupby('year').sum()
launch_df_sum['units_cumulative'] = launch_df_sum['units'].cumsum

# read population data and summarize by year 
pop_df = pd.read_csv("singapore_resident_population.csv", index_col=False)
# drop years before 2004 and keep only total resident data
pop_df = pop_df[(pop_df['year'] >= 2004) & (pop_df['level_1'] == "Total Residents")]
pop_df = pop_df.drop(['level_1','level_2'], axis=1)
pop_df['value'] = pop_df['value'].astype(str).astype(int)
pop_df_sum = pop_df.groupby('year').sum()
pop_df_sum = pop_df_sum.rename(columns={'value':'population'})

# merge population and launch data. Write to file.
df_final = launch_df_sum.merge(pop_df_sum, on='year', how = 'inner')
df_final['units_cumulative'] = df_final['units'].cumsum()
df_final.to_csv("launches_population_data.csv")