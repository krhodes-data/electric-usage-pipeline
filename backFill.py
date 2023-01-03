#For populating the backfilled dates
# Need to amend file reader to separate .csv into smaller chunks
# and store as individual files, which can then be used by dataClean.py
# to clean the data

import pandas as pd
import os
import csv
import glob
import re
from datetime import datetime,date

import difflib

#from dataClean import clean_data

path = '/Users/kevinrhodes/Downloads/'
files = glob.glob(path+"*.csv")
keyword = 'SCE_Usage'
if len(files) > 0:
    latestFile = os.path.basename(max(files, key=os.path.getctime))
    latestFile = 'SCE_Usage_8013433518_12-26-22_to_12-27-22.csv'
    startDate = latestFile.split('_')[3]
    startDate = datetime.strptime(startDate,'%m-%d-%y')
    lastDate = latestFile.split('_')[5].replace('.csv','')
    lastDate = datetime.strptime(lastDate,'%m-%d-%y')
    print(startDate,lastDate)
    if latestFile.startswith(keyword):
        print("Using:",latestFile)
        phrase = f'Data for period starting: {startDate}'
        with open(path+latestFile,'r') as f:
            file = f.readlines()
            #file = ''.join(file)
            print(len(file))
            for lineNum,line in enumerate(file):
                if phrase in line:
                    print(lineNum,line)
            #firstChunk = file.split(phrase)[0]
            #print(len(firstChunk))
            #print(firstChunk)
    else:
        print("Unable to locate valid SCE file.")
else:
    print("No files found - please verify directory.")

#clean_data()