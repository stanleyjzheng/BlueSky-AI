import pandas as pd
import os
import sqlite3

def importSQL():
	workingDirectory = os.path.dirname(os.path.realpath(__file__))
	print(os.path.sep.join([f'{workingDirectory}', 'input', 'FPA_FOD_20170508.sqlite']))
	conn = sqlite3.connect(os.path.sep.join([f'{workingDirectory}', 'input', 'FPA_FOD_20170508.sqlite']))
	df = pd.read_sql_query("SELECT STAT_CAUSE_CODE,DISCOVERY_DOY,CONT_DOY,FIRE_SIZE,FIRE_SIZE_CLASS,LATITUDE,LONGITUDE FROM Fires", con = conn)
	#print(df.head)
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
	train, ver = train.dropna(), ver.dropna()
	trainLabels = train[['CONT_DOY', 'FIRE_SIZE', 'FIRE_SIZE_CLASS']]
	trainLabels.iloc[:, 0] = trainLabels.iloc[:, 0].astype(float).divide(366)
	trainLabels.iloc[:, 1] = trainLabels.iloc[:, 1].astype(float).divide(606945)
	trainLabels.iloc[:, 2] = [ord(x) - 64 for x in trainLabels.iloc[:, 2]]
	trainLabels.iloc[:, 2] = trainLabels.iloc[:, 2].astype(float).divide(7)
	train = train[['DISCOVERY_DOY', 'STAT_CAUSE_CODE', 'LATITUDE', 'LONGITUDE']]
	train.iloc[:, 0] = train.iloc[:, 0].astype(float).divide(366)
	train.iloc[:, 1] = train.iloc[:, 1].astype(float).divide(13)
	train.iloc[:, 2] = [abs(x)-25 for x in train.iloc[:, 2]]
	train.iloc[:, 2] = train.iloc[:, 2].astype(float).divide(48)
	train.iloc[:, 3] = [abs(x)-50 for x in train.iloc[:, 3]]
	train.iloc[:, 3] = train.iloc[:, 3].astype(float).divide(116)
	verLabels = ver[['CONT_DOY', 'FIRE_SIZE', 'FIRE_SIZE_CLASS']]
	verLabels.iloc[:, 0] = verLabels.iloc[:, 0].astype(float).divide(366)
	verLabels.iloc[:, 1] = verLabels.iloc[:, 1].astype(float).divide(606945)
	verLabels.iloc[:, 2] = [ord(x) - 64 for x in verLabels.iloc[:, 2]]
	verLabels.iloc[:, 2] = verLabels.iloc[:, 2].astype(float).divide(7)
	ver = ver[['DISCOVERY_DOY', 'STAT_CAUSE_CODE', 'LATITUDE', 'LONGITUDE']]
	ver.iloc[:, 0] = ver.iloc[:, 0].astype(float).divide(366)
	ver.iloc[:, 1] = ver.iloc[:, 1].astype(float).divide(13)
	ver.iloc[:, 2] = [abs(x)-17 for x in ver.iloc[:, 2]]
	ver.iloc[:, 2] = ver.iloc[:, 2].astype(float).divide(53)
	ver.iloc[:, 3] = [abs(x)-52 for x in ver.iloc[:, 3]]
	ver.iloc[:, 3] = ver.iloc[:, 3].astype(float).divide(116)
	return train, trainLabels, ver, verLabels
# train, trainLabels, verLabels, ver = dataset()	
# print(train.shape)
# print(trainLabels.shape)
# print(verLabels.shape)
# print(ver.shape)