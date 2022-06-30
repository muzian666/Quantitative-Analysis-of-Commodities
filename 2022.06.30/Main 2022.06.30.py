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
import matplotlib.pyplot as plt
#import csv
#from pylab import mpl

#1.全局变量
price = pd.DataFrame(pd.read_csv('./WeekData/NYMEX.csv', encoding = 'utf-8', header = None))
price = price.iloc[1:1776,:]
price.columns = ['date', 'price']
price = price.set_index('date')
price = price['2009-12-25':'2021']
price = price.astype('float')
price_return = price/price.shift(1)-1

#价格曲线
#plt.figure()
#fig = plt.figure(figsize=(12,8))
#ax1 = fig.add_subplot(111)
#ax1.plot((price), '-', label = 'Price')
#ax1.legend(loc = 2)
#ax1.grid()
#ax1.set_xlabel("Date")
#ax1.set_ylabel("Price")

#因子1
factor1_1 = pd.DataFrame(pd.read_csv('./WeekData/factor1-1.csv' , encoding = 'utf-8', header = None))
factor1_2 = pd.DataFrame(pd.read_csv('./MonthData/factor1_2.csv', encoding = 'utf-8', header = None))

factor1_1 = factor1_1.iloc[1:2075,:]
factor1_1.columns = ['date','stock','OPEC Price'] #OPEC Price 属于废弃项
factor1_1 = factor1_1.set_index('date')

stock_change = factor1_1['stock']['2009':'2021']
stock_change = stock_change.astype('float')
stock_change = stock_change.pct_change(periods = 1)
stock_change = stock_change.pct_change(periods = 12)
stock_change = stock_change['2010':'2021']

factor1_1 = factor1_1['2010':'2021']
factor1_1 = factor1_1.astype('float')

#对Factor1_2进行resample
factor1_2 = factor1_2.iloc[1:261,:]
factor1_2 = factor1_2.iloc[:,1]
factor1_2 = factor1_2.astype('float')
factor1_2.index = pd.period_range('31/10/2000', freq='M', periods=260)
factor1_2 = factor1_2.resample('W', convention='end').asfreq()
factor1_2 = factor1_2.interpolate()

#废弃项
#stock_change = factor1_2.pct_change(periods=1)
#stock_change = stock_change.pct_change(periods = 12)
#stock_change = stock_change['2010-01-04':'2020']
#stock_change.index = factor1_1.index

colums = ['Price','Stock Change','Signal For Price','Signal For Stock', 'Price Return','Strategy_Ret','Strategy_Ret2']
MonthlyData_factor1 = pd.DataFrame(data = 0, index = factor1_1.index , columns = colums)
MonthlyData_factor1['Price Return'] = price_return
MonthlyData_factor1['Price'] = price
MonthlyData_factor1['Stock Change'] = stock_change
Signal_factor1 = pd.Series(index = factor1_1.index, data = 0)
loc = 0
for t in range(1,len(MonthlyData_factor1)):
    if ((stock_change[t]>0)&(stock_change[t]>stock_change[t-1])&(abs((stock_change[t])-abs(stock_change[t-1]))<0.535)):
        Signal_factor1[t] = -1
        loc = t
    elif ((stock_change[t]<0)&(stock_change[t]>stock_change[t-1])&(abs((stock_change[t])-abs(stock_change[t-1]))<0.535)):
        Signal_factor1[t] = -1
    elif ((stock_change[t]>0)&(stock_change[t]<stock_change[t-1])&(abs((stock_change[t])-abs(stock_change[t-1]))<0.535)):
        Signal_factor1[t] = 1
    elif ((stock_change[t]<0)&(stock_change[t]<stock_change[t-1])&(abs((stock_change[t])-abs(stock_change[t-1]))<0.535)):
        Signal_factor1[t] = 1
    else:
        Signal_factor1[t] = Signal_factor1[t-1]

#(Signal_factor1[t-1]!=1)&
#    else:
        #Signal_factor1[t] = Signal_factor1[t-1]

MonthlyData_factor1['Signal For Stock'] = Signal_factor1
MonthlyData_factor1['Strategy_Ret'] = MonthlyData_factor1['Price Return']*MonthlyData_factor1['Signal For Stock'].shift(1)
MonthlyData_factor1['Strategy'] = (1+MonthlyData_factor1['Strategy_Ret']).cumprod()

plt.figure()
fig = plt.figure(figsize=(12,8))
ax1 = fig.add_subplot(111)
ax1.plot((MonthlyData_factor1['Price Return']).cumsum(), '-', label = 'Basic')
ax1.plot((MonthlyData_factor1['Strategy_Ret']).cumsum(),'-r', label = 'Choice')
ax1.legend(loc = 2)
#ax1.grid()
ax1.set_xlabel("Date")
ax1.set_ylabel("Choice")

#SR=MonthlyData_factor1['Strategy_Ret'].mean()/MonthlyData_factor1['Strategy_Ret'].std()



