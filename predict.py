# 引入sklearn中自带的保存模块
import os
import joblib
import pandas as pd # 数据分析
#引入测试数据集
df = pd.read_csv("test.csv", sep=',')
#数据预处理
df['time'] = pd.to_datetime(df['time'])
df['time'] = df['time'].apply(lambda x : x.strftime("%Y%m%d")).apply(lambda x: int(x))
x = df.loc[:, df.columns != 'price']
x = pd.get_dummies(x)
df.drop(columns=['price'], inplace=True)
# 导入模型
filedir = "D:\\Desktop\\Python\\Data\\final report\\models\\折叠刀"  # this is the directory of the weapon file
os.chdir(filedir)
filecontant = os.listdir(filedir)  # file name of the weapon
for fileName in filecontant:
    model = joblib.load(fileName)
    name_list = []
    to_list = model.predict(x)
    for i in to_list:
        name_list.append(i)
    df[fileName[:-4]+"price"] = name_list
    print(df)
df.to_csv('D:\\Desktop\\Python\\Data\\final report\\test_output.csv', encoding='utf_8_sig')