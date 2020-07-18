import random
import pandas as pd
import os

def makeTest(df):
	workingDirectory = os.path.dirname(os.path.realpath(__file__))
	with open(filename) as f:
		content = f.readlines(os.path.sep.join([f'{workingDirectory}', 'verification.csv']))
	for i in content:
		