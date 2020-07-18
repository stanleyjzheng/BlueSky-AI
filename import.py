import sqlite3
import pandas as pd
import os

#Make sure you have the dataset in the same directory as this folder with the data inside a folder called input

workingDirectory = os.path.dirname(os.path.realpath(__file__))

print(os.path.sep.join([f'{workingDirectory}', 'input', 'FPA_FOD_20170508.sqlite']))

conn = sqlite3.connect(os.path.sep.join([f'{workingDirectory}', 'input', 'FPA_FOD_20170508.sqlite']))
df = pd.read_sql_query("SELECT FIRE_YEAR,STAT_CAUSE_DESCR,LATITUDE,LONGITUDE,STATE,DISCOVERY_DATE,FIRE_SIZE FROM 'Fires'", con = conn)
print(df.head())