import pandas as pd
import glob
import os

def merge_tables():
    #os.rename(r'C:/Users/nikna/Downloads/BlockFeaturesX.csv',r'C:/Users/nikna/Downloads/BlockFeaturesX (0).csv')
    path = 'C:/Users/nikna/Downloads'
    all_files = glob.glob(path + "/*.csv")
    li = []
    for filename in all_files:
        df = pd.read_csv(filename, index_col=None, header=0)
        li.append(df)
    frame = pd.concat(li, axis=0, ignore_index=True)
    savecsv(frame)

def savecsv(result):
    filename = "Data/CSVs/DataSVMbig.csv"
    result.to_csv(filename, index=False, encoding='utf-8-sig')
    print(filename)

merge_tables()