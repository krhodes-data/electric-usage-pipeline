import pandas as pd
import os
import csv
import glob

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
        df.iloc[:,1].replace(value='',regex='"',inplace=True)
        df.iloc[:,1] = pd.to_numeric(df.iloc[:,1])
    except Exception as e:
        print("Exception:",e)
        if len(latestFile) >= 45:
            print("File length seems short - please verify file contains data.")
        else:
            print("Some other error occurred - please validate file.")
    return df


cleanedFileDirectory = '/Users/kevinrhodes/'
dfR = clean_data(energyReceived)
#dfR.to_parquet()
dfD = clean_data(energyDelivered)
