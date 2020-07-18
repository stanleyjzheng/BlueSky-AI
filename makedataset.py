import pandas as pd
import os
import sqlite3


def importSQL():
	workingDirectory = os.path.dirname(os.path.realpath(__file__))
	print(os.path.sep.join([f'{workingDirectory}', 'input', 'FPA_FOD_20170508.sqlite']))
	conn = sqlite3.connect(os.path.sep.join([f'{workingDirectory}', 'input', 'FPA_FOD_20170508.sqlite']))
	df = pd.read_sql_query("SELECT DISCOVERY_DOY,CONT_DOY,FIRE_SIZE,LATITUDE,LONGITUDE,STATE FROM Fires", con = conn)
	print(df.head())
	print
	return df

def makeTest(df):
	workingDirectory = os.path.dirname(os.path.realpath(__file__))
	with open(os.path.sep.join([f'{workingDirectory}', 'verification.txt']), 'r') as f:
		content = f.readlines() 
	content = [int(x.strip()) for x in content] 
	ver = df.loc[content]
	train = pd.concat([ver,df]).drop_duplicates(keep=False)
	return train, ver

def dataset():
	train, ver = makeTest(importSQL())
	return train, ver

train, ver = dataset()
print(train.shape)
print(ver.shape)