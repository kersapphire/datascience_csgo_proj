import pandas as pd
import os
import numpy as np
import matplotlib.pyplot as plt
import warnings
from sklearn.model_selection import train_test_split
import warnings
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import Lasso
from sklearn.linear_model import Ridge
from sklearn.neural_network import MLPRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.tree import ExtraTreeRegressor
from xgboost import XGBRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.ensemble import AdaBoostRegressor
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.ensemble import BaggingRegressor

# filter warnings
warnings.filterwarnings('ignore')
# 正常显示中文
from pylab import mpl

mpl.rcParams['font.sans-serif'] = ['SimHei']

# 正常显示符号
from matplotlib import rcParams

rcParams['axes.unicode_minus'] = False

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
tdf = pd.DataFrame()
tdf['ModelName'] = ['Lasso', 'DecisionTree', 'XGBoost', 'RandomForest', 'GradientBoost', 'MLPRegressor', 'ExtraTree',
                    'AdaBoost', 'Bagging', 'LinearRegression', 'Ridge']
tdf.set_index('ModelName', inplace=True)
print(tdf)

filedir = "D:\\Desktop\\Python\\Data\\final report\\cleaned_data"  # this is the directory of the weapon file
os.chdir(filedir)
filecontant = os.listdir(filedir)  # file name of the weapon
for fileName in filecontant:
    data = pd.read_csv(fileName)  # 还有这里业绩的改

    data['time'] = pd.to_datetime(data['time'])
    data['time'] = data['time'].apply(lambda x: x.strftime("%Y%m%d")).apply(lambda x: int(x))

    x = data.loc[:, data.columns != 'price']
    y = data.loc[:, 'price']
    mean_cols = x.mean()
    std_cols = x.std()
    mean_axis = y.mean()
    std_axis = y.std()
    x = x.fillna(mean_cols)  # 填充缺失值
    # x_dum = pd.get_dummies(x)  # 独热编码
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.3, random_state=1)

    df = pd.DataFrame(columns=['ModelName', fileName[8:-3] + 'Score'])  # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    # 不做处理
    models = [Lasso(), DecisionTreeRegressor(), XGBRegressor(), RandomForestRegressor(), GradientBoostingRegressor()]
    models_str = ['Lasso', 'DecisionTree', 'XGBoost', 'RandomForest', 'GradientBoost']
    score_ = []

    for name, model in zip(models_str, models):
        print('开始训练模型：' + name)
        model = model  # 建立模型
        model.fit(x_train, y_train)
        y_pred = model.predict(x_test)
        score = model.score(x_test, y_test)
        score_.append(str(score)[:5])
        print(name + ' 得分:' + str(score))
        tmpdf = pd.DataFrame({'ModelName': name, fileName[8:-3] + 'Score': str(score)}, index=['0'])
        df = df.append(tmpdf, ignore_index=True)

    # 标准化
    models = [MLPRegressor(alpha=20), ExtraTreeRegressor(), AdaBoostRegressor(), BaggingRegressor()]
    models_str = ['MLPRegressor', 'ExtraTree', 'AdaBoost', 'Bagging']
    x1 = (x - mean_cols) / std_cols
    y1 = (y - mean_axis) / std_axis
    # x1_dum = pd.get_dummies(x1)
    x_train, x_test, y_train, y_test = train_test_split(x1, y1, test_size=0.3, random_state=1)
    for name, model in zip(models_str, models):
        print('开始训练模型：' + name)
        model = BaggingRegressor()  # 建立模型
        model.fit(x_train, y_train)
        y_pred = model.predict(x_test)
        score = model.score(x_test, y_test)
        score_.append(str(score)[:5])
        print(name + ' 得分:' + str(score))
        tmpdf = pd.DataFrame({'ModelName': name, fileName[8:-3] + 'Score': str(score)}, index=['0'])
        df = df.append(tmpdf, ignore_index=True)

    # 平滑处理
    models = [LinearRegression(), Ridge()]
    models_str = ['LinearRegression', 'Ridge']
    y2 = np.log(y)
    x_train, x_test, y_train, y_test = train_test_split(x, y2, test_size=0.3, random_state=1)

    for name, model in zip(models_str, models):
        print('开始训练模型：' + name)
        model = BaggingRegressor()  # 建立模型
        model.fit(x_train, y_train)
        y_pred = model.predict(x_test)
        score = model.score(x_test, y_test)
        score_.append(str(score)[:5])
        print(name + ' 得分:' + str(score))
        tmpdf = pd.DataFrame({'ModelName': name, fileName[8:-3] + 'Score': str(score)}, index=['0'])
        df = df.append(tmpdf, ignore_index=True)
    df.set_index('ModelName', inplace=True)
    print(df)
    tdf = tdf.merge(df, how='inner', left_index=True, right_index=True)
    print(tdf)
print(tdf)

outputdir = "D:\\Desktop\\Python\\Data\\final report"
tdf.to_csv(outputdir + '\\' + 'total_model_score.csv', encoding='utf_8_sig')
