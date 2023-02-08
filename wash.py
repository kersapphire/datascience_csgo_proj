import os

import pandas as pd
from datetime import datetime

custom_date_parser = lambda x: datetime.strptime(x, "%m-%d-%Y %H:%M")
month = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

filedir = "D:\\Desktop\\Python\\Data\\final report\\11个箱子，三把刀\\knife"  # this is the directory of the weapon file
filecontant = os.listdir(filedir)  # file name of the weapon
for fileName in filecontant:
    print("this is knife " + fileName)
    df = pd.read_csv(filedir + '\\' + fileName)
    df = df.dropna()
    for i in range(len(month)):
        df['time'] = df['time'].str.replace(month[i], str(i + 1), regex=False)
    df['time'] = pd.to_datetime(df['time'], format="%m %d %Y %H %M")

    print(df)
    df['time'] = df['time'].dt.date
    print(df)

    df = df.groupby(by='time').mean()
    df.sort_index(ascending=True, inplace=True)

    print(df)

    boxfiledir = "D:\\Desktop\\Python\\Data\\final report\\11个箱子，三把刀\\box"    # directory where you put all and only all the box files
    boxfilecontant = os.listdir(boxfiledir)             # filename of the boxs will be fetched automatically
    n = 1
    for boxfilename in boxfilecontant:
        print('this is file ' + boxfilename)
        df_box = pd.read_csv(boxfiledir + '\\' + boxfilename)
        df_box = df_box.dropna()
        for i in range(len(month)):
            df_box['time'] = df_box['time'].str.replace(month[i], str(i + 1), regex=False)
        df_box['time'] = pd.to_datetime(df_box['time'], format="%m %d %Y %H %M")

        print(df_box)
        df_box['time'] = df_box['time'].dt.date
        print(df_box)

        df_box = df_box.groupby(by='time').mean()
        df_box.sort_index(ascending=True, inplace=True)

        outputfiledir = "D:\\Desktop\\Python\\Data\\final report\\cleaned_data_box"
        df_box.to_csv(outputfiledir + '\\' + 'cleaned_' + boxfilename, encoding='utf_8_sig')

        print(df_box)
        df_box = df_box.drop(columns=['number'])
        col_name = "box_price_" + str(n)
        df_box.rename(columns={"boxprice": col_name}, inplace=True)
        print(df_box)
        df = df.merge(df_box, how='inner', left_index=True, right_index=True)
        n = n + 1

    print(df)
    cleanedfiledir = "D:\\Desktop\\Python\\Data\\final report\\cleaned_data"
    df.to_csv(cleanedfiledir + '\\' + 'cleaned_' + fileName, encoding='utf_8_sig')