#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 23 09:28:48 2022

@author: muzian
"""

'''
5个因子
1.原油库存变动+油价 --> 基本面因子信号 --> 信号的发出取决与否取决于当期月均开工率与8个月前的月均开工率的高低情况。
2.原油价格+主要国家M2 --> 流动性因子信号 --> 判断当前广义货币同比处于过去一个季度的历史分为数决定发出信号与否。
3.原油价格+CFTC投机净持仓 --> 情绪因子信号 --> 衡量历史分为数 --> 当投机净持仓数据在回测窗口内处于高位，投机力量看好油价上涨，情绪因子发出看多信号。
4.原油价格+美元指数 --> 美元因子信号 --> 过去一个月平均美元指数低于之前一个月的平均值时，入场做多，反之做空。
5.原油价格+标普500（VIX）--> 风险因子信号 --> VIX大于观测窗口数据的55分位数时，做空；VIX小雨观测窗口数据45分位数时，做多。VIX大于17时才发出入场信号。
'''

# 数据导入
import numpy as np
import pandas as pd
#import csv
import matplotlib.pyplot as plt
#from pylab import mpl

#1.因子1
#1.1 原油库存变动
#读取CSV至字典
factor1_1 = pd.DataFrame(pd.read_csv('factor1-1.csv', encoding = 'utf-8', header = None))
factor1_2 = pd.DataFrame(pd.read_csv('factor1_2.csv', encoding = 'utf-8', header = None))
Adj_num_for_factor1 = np.arange(0,575)
time_factor_1 = pd.to_datetime(factor1_1.iloc[318:450,0])
time_factor_2 = pd.to_datetime(factor1_1.iloc[317:450,0])
stock_change = factor1_1.iloc[318:450,1]
stock_change = stock_change.astype('float')
stock_change.index = time_factor_1
price = factor1_1.iloc[317:450,2]
price.index = time_factor_2
price = price.astype('float')
#stock_change = pd.Series(data = factor1.iloc[385:3235,1], index = time_factor_1)
#price = pd.Series(data = factor1.iloc[385:3235,2], index = time_factor_1)
start_ratio = factor1_2.iloc[112:244,1]
start_ratio.index = time_factor_1

#信号判断
colums = ['Price','Stock Change','Signal For Price','Signal For Stock', 'Price Return','Strategy_Ret','Strategy_Ret2']
MonthlyData_factor1 = pd.DataFrame(data = 0, index = time_factor_1, columns = colums)
MonthlyData_factor1['Price Return'] = price / price.shift(1)-1
MonthlyData_factor1['Price'] = price
MonthlyData_factor1['Stock Change'] = stock_change
Signal_factor1 = pd.Series(index = time_factor_1, data = 0)
loc = 0
for t in range(1,len(MonthlyData_factor1)):
    if (Signal_factor1[t-1]!=1)&((stock_change[t]>stock_change[t-1])):
        Signal_factor1[t] = 1
        loc = t
    elif (Signal_factor1[t-1]!=0)&((stock_change[t]<stock_change[t-1])):
        Signal_factor1[t] = 0
    else:
        Signal_factor1[t] = Signal_factor1[t-1]
MonthlyData_factor1['Signal For Stock'] = Signal_factor1
MonthlyData_factor1['Strategy_Ret'] = MonthlyData_factor1['Price Return']*MonthlyData_factor1['Signal For Stock'].shift(1)
MonthlyData_factor1['Strategy'] = (1+MonthlyData_factor1['Strategy_Ret']).cumprod()

plt.figure()
fig = plt.figure(figsize=(12,8))
ax1 = fig.add_subplot(111)
ax1.plot((MonthlyData_factor1['Price Return']).cumsum(), '-', label = 'Basic')
ax1.plot((MonthlyData_factor1['Strategy_Ret']).cumsum(),'-r', label = 'Choice')
ax1.legend(loc = 2)
ax1.grid()
ax1.set_xlabel("Date")
ax1.set_ylabel("jczs")


Signal_factor1_2 = pd.Series(index = time_factor_1, data = 0)
for t in range(8,len(MonthlyData_factor1)):
    if (Signal_factor1_2[t-8]!=1)&((start_ratio[t]<start_ratio[t-8])):
        Signal_factor1_2[t] = 1
        loc = t
    elif(Signal_factor1_2[t-8]!=0)&((start_ratio[t]>start_ratio[t-8])):
        Signal_factor1_2[t] = -1
    else:
        Signal_factor1_2[t] = Signal_factor1_2[t-8]
MonthlyData_factor1['Signal For Price'] = Signal_factor1_2
MonthlyData_factor1['Strategy_Ret2'] = MonthlyData_factor1['Price Return']*MonthlyData_factor1['Signal For Price'].shift(1)
MonthlyData_factor1['Strategy2'] = (1+MonthlyData_factor1['Strategy_Ret2']).cumprod()

plt.figure()
fig = plt.figure(figsize=(12,8))
ax1 = fig.add_subplot(111)
ax1.plot((MonthlyData_factor1['Price Return']).cumsum(), '-', label = 'Basic')
ax1.plot((MonthlyData_factor1['Strategy_Ret2']).cumsum(),'-r', label = 'Choice')
ax1.legend(loc = 2)
ax1.grid()
ax1.set_xlabel("Date")
ax1.set_ylabel("jczs")


#2.因子2
#2.1 M2值计算
#读取CSV至字典
TotalM2 = pd.DataFrame(pd.read_csv('M2-2.csv', encoding = 'utf-8', header = None))
factor2_NYMEX = pd.DataFrame(pd.read_csv('factor4.csv', encoding = 'utf-8', header = None))
a = np.arange(0,132)
#a = a.astype('float')
AdjM2 = TotalM2[601:745]
#AdjM2.index = a
time = pd.to_datetime(AdjM2.iloc[0:144,0])
time_1 = pd.to_datetime(AdjM2.iloc[12:144,0])
time_2 = pd.to_datetime(AdjM2.iloc[0:132,0])
time_factor_2_NYMEX = pd.to_datetime(factor2_NYMEX.iloc[468:601,0])
#time_2 = pd.to_datetime(AdjM2.iloc[12:144,0])
#time = pd.to_datetime(AdjM2.iloc[12:156,0])
#set data time & index!!!!

#人民币M2
CNYM2 = pd.Series(data = AdjM2.iloc[:,1])
CNYM2 = CNYM2.astype('float')
CNYM2 = CNYM2.astype('float')
CNYM2 = CNYM2

#美元M2
USDM2 = pd.Series(data = AdjM2.iloc[:,2])
USDM2 = USDM2.astype('float')
USD2CNY = pd.Series(data = AdjM2.iloc[:,6])
USD2CNY = USD2CNY.astype('float')
USDM2 = USDM2*USD2CNY*10

#欧元M2
EURM2 = pd.Series(data = AdjM2.iloc[:,3])
EURM2 = EURM2.astype('float')
EUR2CNY = pd.Series(data = AdjM2.iloc[:,7])
EUR2CNY = EUR2CNY.astype('float')
EURM2 = EURM2*EUR2CNY/10

#日元M2
JPNM2 = pd.Series(data = AdjM2.iloc[:,4])
JPNM2 = JPNM2.astype('float')
JPN2CNY = pd.Series(data = AdjM2.iloc[:,5])
JPN2CNY = JPN2CNY.astype('float')
JPNM2 = JPNM2*100*JPN2CNY

#计算中美日欧M2
AdjFinalM2 = CNYM2 + USDM2 + EURM2 + JPNM2
AdjFinalM2 = AdjFinalM2.astype('float')
AdjFinalM2.index = time
AdjFinalM2_1 = AdjFinalM2[0:132]
AdjFinalM2_2 = pd.Series(data = AdjFinalM2[12:144])
AdjFinalM2_1.index = a
AdjFinalM2_2.index = a
#AdjFinalM2_2 = AdjFinalM2_2.astype('float')
FinalM2 = (AdjFinalM2_2 - AdjFinalM2_1)/AdjFinalM2_1
FinalM2.index = time_1

#NYMEX
Factor_2_NYMEX_Price = factor2_NYMEX.iloc[468:601,2]
Factor_2_NYMEX_Price = Factor_2_NYMEX_Price.astype('float')
Factor_2_NYMEX_Price.index = time_factor_2_NYMEX
colums = ['NYMEX','M2','M2 Signal','Price Return Factor 2','Strategy Ret Factor 2', 'Strategy Factor 2']
MonthlyData_factor2 = pd.DataFrame(data = 0, index = time_factor_2_NYMEX, columns = colums)
MonthlyData_factor2['NYMEX'] = Factor_2_NYMEX_Price
MonthlyData_factor2['M2'] = FinalM2
MonthlyData_factor2['Price Return Factor 2'] = MonthlyData_factor2['NYMEX'] / MonthlyData_factor2['NYMEX'].shift(1)-1

Signal_factor_2 = pd.Series(index = time_factor_2_NYMEX, data = 0)
loc = 0
for t in range(4, len(MonthlyData_factor2)):
    if (Signal_factor_2[t-4]!=1)&((np.percentile(np.array([MonthlyData_factor2['M2'][t-3],MonthlyData_factor2['M2'][t-2],MonthlyData_factor2['M2'][t-1]]),50))<MonthlyData_factor2['M2'][t]):
        Signal_factor_2[t] = 1
        loc = t
    elif (Signal_factor_2[t-4]!=0)&((np.percentile(np.array([MonthlyData_factor2['M2'][t-3],MonthlyData_factor2['M2'][t-2],MonthlyData_factor2['M2'][t-1]]),75))>MonthlyData_factor2['M2'][t]):
        Signal_factor_2[t] = -1
    else:
        Signal_factor_2[t] = Signal_factor_2[t-3]

MonthlyData_factor2['M2 Signal'] = Signal_factor_2
MonthlyData_factor2['Strategy Ret Factor 2'] = MonthlyData_factor2['Price Return Factor 2']*MonthlyData_factor2['M2 Signal'].shift(1)
MonthlyData_factor2['Strategy Factor 2'] = (1+MonthlyData_factor2['Strategy Ret Factor 2']).cumprod()

plt.figure()
fig = plt.figure(figsize=(12,8))
ax1 = fig.add_subplot(111)
ax1.plot((MonthlyData_factor2['Price Return Factor 2']).cumsum(), '-', label = 'Basic')
ax1.plot((MonthlyData_factor2['Strategy Ret Factor 2']).cumsum(),'-r', label = 'Choice')
ax1.legend(loc = 2)
ax1.grid()
ax1.set_xlabel("Date")
ax1.set_ylabel("jczs")


#3.因子3
factor3_Motion = pd.DataFrame(pd.read_csv('Factor3.csv', encoding = 'utf-8', header = None))
factor3_NYMEX = pd.DataFrame(pd.read_csv('factor4.csv', encoding = 'utf-8', header = None))
time_factor_3= pd.to_datetime(factor3_NYMEX.iloc[468:601,0])
colums = ['NYMEX','Motion','Motion Signal','Price Return Factor 3','Strategy Ret Factor 3', 'Strategy']
MonthlyData_Factor3 = pd.DataFrame(data = 0, index = time_factor_3, columns = colums)
NYMEX_Price = factor3_NYMEX.iloc[468:601,2]
NYMEX_Price = NYMEX_Price.astype('float')
NYMEX_Price.index = time_factor_3
Motion_1 = factor3_Motion.iloc[289:422,1]
Motion_1 = Motion_1.astype('float')
Motion_2 = factor3_Motion.iloc[289:422,2]
Motion_2 = Motion_2.astype('float')
Motion = Motion_1 + Motion_2
Motion.index = time_factor_3
MonthlyData_Factor3['NYMEX'] = NYMEX_Price
MonthlyData_Factor3['Motion'] = Motion
MonthlyData_Factor3['Price Return Factor 3'] = MonthlyData_Factor3['NYMEX'] / MonthlyData_Factor3['NYMEX'].shift(1)-1
#Motion_Array = np.array([MonthlyData_Factor3['Motion']])
#Motion_Array = Motion_Array.astype('float')
#Percentile_Motion = np.percentile(Motion_Array,70)
Signal_factor_3 = pd.Series(index = time_factor_3, data = 0)
loc = 0
for t in range(1,len(MonthlyData_Factor3)):
    if (Signal_factor_3[t-1]!=1)&((MonthlyData_Factor3['Motion'][t-1])<(np.percentile(np.array([MonthlyData_Factor3['Motion'][0:t]]),60))):
        Signal_factor_3[t] = 1
        loc = t
    elif (Signal_factor_3[t-1]!=0)&((MonthlyData_Factor3['Motion'][t-1])>(np.percentile(np.array([MonthlyData_Factor3['Motion'][0:t]]),60))):
        Signal_factor_3[t] = -1
    else:
        Signal_factor_3[t] = Signal_factor_3[t-1]
MonthlyData_Factor3['Motion Signal'] = Signal_factor_3
MonthlyData_Factor3['Strategy Ret Factor 3'] = MonthlyData_Factor3['Price Return Factor 3']*MonthlyData_Factor3['Motion Signal'].shift(1)
MonthlyData_Factor3['Strategy'] = (1+MonthlyData_Factor3['Strategy Ret Factor 3']).cumprod()

plt.figure()
fig = plt.figure(figsize=(12,8))
ax1 = fig.add_subplot(111)
ax1.plot((MonthlyData_Factor3['Price Return Factor 3']).cumsum(), '-', label = 'Basic')
ax1.plot((MonthlyData_Factor3['Strategy Ret Factor 3']).cumsum(),'-r', label = 'Choice')
ax1.legend(loc = 2)
ax1.grid()
ax1.set_xlabel("Date")
ax1.set_ylabel("jczs")


#4.因子4
factor4 = pd.DataFrame(pd.read_csv('factor4.csv', encoding = 'utf-8', header = None))
time_factor_4 = pd.to_datetime(factor4.iloc[468:601,0])
A_index = factor4.iloc[468:601,1]
A_index = A_index.astype('float')
A_index.index = time_factor_4
NYMEX_Price = factor4.iloc[468:601,2]
NYMEX_Price = NYMEX_Price.astype('float')
NYMEX_Price.index = time_factor_4
colums = ['NYMEX','USD Index','Index Signal','Price Return Factor 4','Strategy Ret Factor 4', 'Strategy']
MonthlyData_factor4 = pd.DataFrame(data = 0, index = time_factor_4, columns = colums)
MonthlyData_factor4['NYMEX'] = NYMEX_Price
MonthlyData_factor4['USD Index'] = A_index
MonthlyData_factor4['Price Return Factor 4'] = MonthlyData_factor4['NYMEX'] / MonthlyData_factor4['NYMEX'].shift(1)-1

Signal_factor_4 = pd.Series(index = time_factor_4, data = 0)
loc = 0
for t in range(1,len(MonthlyData_factor4)):
    if (Signal_factor_4[t-1]!=1)&((MonthlyData_factor4['USD Index'][t]<MonthlyData_factor4['USD Index'][t-1])):
        Signal_factor_4[t] = 1
        loc = t
    elif (Signal_factor_4[t-1]!=0)&((MonthlyData_factor4['USD Index'][t]>MonthlyData_factor4['USD Index'][t-1])):
        Signal_factor_4[t] = -1
    else:
        Signal_factor_4[t] = Signal_factor_4[t-1]
MonthlyData_factor4['Index Signal'] = Signal_factor_4
MonthlyData_factor4['Strategy Ret Factor 4'] = MonthlyData_factor4['Price Return Factor 4']*MonthlyData_factor4['Index Signal'].shift(1)
MonthlyData_factor4['Strategy'] = (1+MonthlyData_factor4['Strategy Ret Factor 4']).cumprod()

plt.figure()
fig = plt.figure(figsize=(12,8))
ax1 = fig.add_subplot(111)
ax1.plot((MonthlyData_factor4['Price Return Factor 4']).cumsum(), '-', label = 'Basic')
ax1.plot((MonthlyData_factor4['Strategy Ret Factor 4']).cumsum(),'-r', label = 'Choice')
ax1.legend(loc = 2)
ax1.grid()
ax1.set_xlabel("Date")
ax1.set_ylabel("jczs")

#5.因子5
factor5 = pd.DataFrame(pd.read_csv('VIX.csv', encoding = 'utf-8', header = None))
time_factor_5 = pd.to_datetime(factor5.iloc[26:158,0])
factor5_NYMEX = pd.DataFrame(pd.read_csv('factor4.csv', encoding = 'utf-8', header = None))
time_factor_5_NYMEX = pd.to_datetime(factor5_NYMEX.iloc[468:601,0])
Factor5_NYMEX_Price = factor5_NYMEX.iloc[468:601,2]
Factor5_NYMEX_Price = Factor5_NYMEX_Price.astype('float')
Factor5_NYMEX_Price.index = time_factor_5_NYMEX
VIX_index = factor5.iloc[26:158,1]
VIX_index = VIX_index.astype('float')
VIX_index.index = time_factor_5
colums = ['NYMEX','VIX Index','Index Signal','Price Return Factor 5','Strategy Ret Factor 5', 'Strategy']
MonthlyData_Factor5 = pd.DataFrame(data = 0, index = time_factor_5, columns = colums)
MonthlyData_Factor5['NYMEX'] = Factor5_NYMEX_Price
MonthlyData_Factor5['VIX Index'] = VIX_index
MonthlyData_Factor5['Price Return Factor 5'] = MonthlyData_Factor5['NYMEX'] / MonthlyData_Factor5['NYMEX'].shift(1)-1
#VIX_Array = np.array([MonthlyData_Factor5['VIX Index']])
#VIX_Array = VIX_Array.astype('float')
#Percentile_VIX = np.percentile(VIX_Array,70)

Signal_factor_5 = pd.Series(index = time_factor_5, data = 0)
loc = 0
for t in range(1, len(MonthlyData_Factor5)):
    if (Signal_factor_5[t-1]!=1)&((np.percentile(np.array([MonthlyData_Factor5['VIX Index']]),55))<MonthlyData_Factor5['VIX Index'][t])&((np.percentile(np.array([MonthlyData_Factor5['VIX Index']]),17))<MonthlyData_Factor5['VIX Index'][t]):
        Signal_factor_5[t] = 1
        loc = t
    elif (Signal_factor_5[t-1]!=0)&((np.percentile(np.array([MonthlyData_Factor5['VIX Index']]),45))>MonthlyData_Factor5['VIX Index'][t]):
        Signal_factor_5[t] = -1
    else:
        Signal_factor_5[t] = Signal_factor_5[t-1]

MonthlyData_Factor5['Index Signal'] = Signal_factor_5
MonthlyData_Factor5['Strategy Ret Factor 5'] = MonthlyData_Factor5['Price Return Factor 5']*MonthlyData_Factor5['Index Signal'].shift(1)
MonthlyData_Factor5['Strategy'] = (1+MonthlyData_Factor5['Strategy Ret Factor 5']).cumprod()

plt.figure()
fig = plt.figure(figsize=(12,8))
ax1 = fig.add_subplot(111)
ax1.plot((MonthlyData_Factor5['Price Return Factor 5']).cumsum(), '-', label = 'Basic')
ax1.plot((MonthlyData_Factor5['Strategy Ret Factor 5']).cumsum(),'-r', label = 'Choice')
ax1.legend(loc = 2)
ax1.grid()
ax1.set_xlabel("Date")
ax1.set_ylabel("jczs")

T_Signal_Colunms = ['Factor 1 Signal', 'Factor 2 Signal','Factor 3 Signal','Factor 4 Signal','Factor 5 Signal', 'Factor 6 Signal','Average Signal','Strategy']
T_Signal = pd.DataFrame(data = 0, index = time_factor_1, columns = T_Signal_Colunms)
T_Signal['Factor 1 Signal'] = MonthlyData_factor1['Signal For Stock']
T_Signal['Factor 2 Signal'] = MonthlyData_factor1['Signal For Price']
T_Signal['Factor 3 Signal'] = MonthlyData_factor2['M2 Signal']
T_Signal['Factor 4 Signal'] = MonthlyData_Factor3['Motion Signal']
T_Signal['Factor 5 Signal'] = MonthlyData_factor4['Index Signal']
T_Signal['Factor 6 Signal'] = MonthlyData_Factor5['Index Signal']
T_Signal['Average Signal'] = (T_Signal['Factor 1 Signal']+T_Signal['Factor 2 Signal']+T_Signal['Factor 3 Signal']+T_Signal['Factor 4 Signal']+T_Signal['Factor 5 Signal']+T_Signal['Factor 6 Signal'])/6

T_Signal['Price'] = NYMEX_Price
T_Signal['Price Return'] = MonthlyData_factor4['Price Return Factor 4']
T_Signal['Strategy Ret Factor'] = T_Signal['Price Return']*T_Signal['Average Signal'].shift(1)
T_Signal['Strategy'] = (1+T_Signal['Strategy Ret Factor']).cumprod()

plt.figure()
fig = plt.figure(figsize=(12,8))
ax1 = fig.add_subplot(111)
ax1.plot((T_Signal['Price Return']).cumsum(), '-k', label = 'Basic')
ax1.plot((T_Signal['Strategy Ret Factor']).cumsum(),'-r', label = 'Total Choice')
ax1.plot((MonthlyData_factor1['Strategy_Ret2']).cumsum(),'-y', label = 'Choice Factor 1')
ax1.plot((MonthlyData_factor1['Strategy_Ret2']).cumsum(),'-b', label = 'Choice Factor 1-2')
ax1.plot((MonthlyData_factor2['Strategy Ret Factor 2']).cumsum(),'-g', label = 'Choice Factor 2')
ax1.plot((MonthlyData_Factor3['Strategy Ret Factor 3']).cumsum(),'-m', label = 'Choice Factor 3')
ax1.plot((MonthlyData_factor4['Strategy Ret Factor 4']).cumsum(),'-c', label = 'Choice Factor 4')
ax1.plot((MonthlyData_Factor5['Strategy Ret Factor 5']).cumsum(),color = 'deepskyblue', label = 'Choice Factor 5')

ax1.legend(loc = 2)
ax1.grid()
ax1.set_xlabel("Date")
ax1.set_ylabel("jczs")




