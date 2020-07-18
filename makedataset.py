import pandas as pd
import os
import sqlite3


def importSQL():
	workingDirectory = os.path.dirname(os.path.realpath(__file__))
	print(os.path.sep.join([f'{workingDirectory}', 'input', 'FPA_FOD_20170508.sqlite']))
	conn = sqlite3.connect(os.path.sep.join([f'{workingDirectory}', 'input', 'FPA_FOD_20170508.sqlite']))
	df = pd.read_sql_query("SELECT DISCOVERY_DOY,CONT_DOY,FIRE_SIZE,LATITUDE,LONGITUDE,STATE FROM Fires", con = conn)
	print(df.head())
	return df

def makeTest(df):
	workingDirectory = os.path.dirname(os.path.realpath(__file__))
	with open(os.path.sep.join([f'{workingDirectory}', 'verification.txt']), 'r') as f:
		content = f.readlines() 
	content = [int(x.strip()) for x in content] 
	ver = df.loc[content]
	train = pd.concat([ver, df])
	train = df.reset_index(drop=True)
	train_gpby = df.groupby(list(df.columns))
	idx = [x[0] for x in train_gpby.groups.values() if len(x) == 1]
	train = df.reindex(idx)
	return train, ver

def dataset():
	train, ver = makeTest(importSQL())
	return train, ver

dataset()
print(train.shape)
print(ver.shape)