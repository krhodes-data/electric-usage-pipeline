import pandas as pd

import os
import csv
import glob
from datetime import datetime,timedelta
from pytz import timezone

# Suppress future warnings from pandas
import warnings
warnings.filterwarnings(action='ignore',
                        category=FutureWarning
)

path = '/Users/kevinrhodes/Downloads/'
files = glob.glob(path+"*.csv")
keyword = 'SCE_Usage'
if len(files) > 0:
    latestFile = os.path.basename(max(files, key=os.path.getctime))
    if latestFile.startswith(keyword):
        print("Using:",latestFile)
        with open(path+latestFile,'r') as f:
            energyReceived = []
            energyDelivered = []
            for lineNum,line in enumerate(f):
                if lineNum in range(0,12):
                    continue
                elif lineNum >= 111:
                    energyReceived.append(line.strip())
                else:
                    energyDelivered.append(line.strip())
    else:
        print("Unable to locate valid SCE file.")
else:
    print("No files found - please verify directory.")



def clean_data(dataList):
    try:
        df = pd.DataFrame(dataList)
        df = df.iloc[1:,:]
        colList = list(df.iloc[0].str.split(','))
        colList = [col.replace('\xa0',' ').replace(' ','_').replace('__','_').lower() for col in colList[0]]
        df = df[0].str.split(',',expand=True)
        df.columns = colList
        df = df.iloc[1:,:].dropna().reset_index(drop=True)
        df.iloc[:,0].replace(value='',regex='to.*',inplace=True)
        df.iloc[:,0].replace(value='',regex='"',inplace=True)
        df.iloc[:,0] = pd.to_datetime(df.iloc[:,0],utc=True)
        df.iloc[:,0] = df.iloc[:,0].map(lambda x: x.astimezone('US/Pacific')).map(lambda x: x + timedelta(hours=8))
        df.iloc[:,1].replace(value='',regex='"',inplace=True)
        df.iloc[:,1] = pd.to_numeric(df.iloc[:,1])
    except Exception as e:
        print("Exception:",e)
        if len(latestFile) >= 45:
            print("File length seems short - please verify file contains data.")
        else:
            print("Some other error occurred - please validate file.")
    return df

# Gets date of file and converts to YYYY-MM-DD string
fileDate = latestFile.split('_')[3]
fileDate = datetime.strptime(fileDate,'%m-%d-%y')
fileDate = str(datetime.date(fileDate))
cleanedFileDirectory = '/Users/kevinrhodes/Desktop/cleanedFiles/'
if os.path.exists(cleanedFileDirectory):
    pass
else:
    os.mkdir(cleanedFileDirectory)

dfR = clean_data(energyReceived)
#print(dfR.iloc[:,0])
dfR.to_parquet(cleanedFileDirectory+'energy_received_'+fileDate,engine='pyarrow')
dfD = clean_data(energyDelivered)
dfD.to_parquet(cleanedFileDirectory+'energy_generated_'+fileDate,engine='pyarrow')