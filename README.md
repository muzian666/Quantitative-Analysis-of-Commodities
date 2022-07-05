# 大宗商品分析（原油）

是一个小白的自我学习记录，记录自己的学习过程

真的是小白，没学过py，纯纯的一边摸索一边学习一边写，写的不好，勿喷

尝试复刻研报：https://mp.weixin.qq.com/s/TW9ruRTTqupAxkvW86YZvA

数据来源：Wind金融终端、同花顺iFinD（手动摘取，没用API）

# 总结
## 整体逻辑

大概的逻辑是这个样子，首先导入需要用到的库文件：

```python
import numpy as np #用于做数学计算
import pandas as pd #用于做数据处理的
import matplotlib.pyplot as plt #用于画图的
import matplotlib.ticker as mticker #用于对x轴密度进行处理的
```

导入完库文件后，因为整篇内容都有一个核心参数就是原油价格，这里的原油价格我们使用布朗特原油，所以这里的价格可以作为全局变量，放在第一个位置。

```python
price = pd.DataFrame(pd.read_csv('./WeekData/NYMEX_1.csv', encoding = 'utf-8', header = None))  #读取csv文件
price = price.iloc[1:1777,:] #去掉首行的名称和尾行的水印
price.columns = ['date', 'price']  #对两列进行命名
price = price.set_index('date') #把时间作为表格的index
price = price['2009-12-25':'2021'] #选取需要的时间段
price = price.astype('float')  #把数据类型转换为浮点数
price_return = price/price.shift(1)-1  #计算价格的Return
```

然后就是计算第一个因子啦～

## 基本面因子

第一个因子因为具有两个指标，库存指标与需求指标，需要先对这两个指标的信号做出一定的反应，然后将信号输出。

### 库存指标

```python
for t in range(1,len(WeekData_factor1)):
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
```

### 需求指标

```python
for t in range(8, len(factor1_2)):
    if abs(factor1_2[t] - factor1_2[t-8])>5.1:
        Signal_factor1_2[t] = 1
        loc = t
    elif abs(factor1_2[t] - factor1_2[t-8])<5.1:
        Signal_factor1_2[t] = -1
    else:
        Signal_factor1_2[t] = Signal_factor1_2 [t-1]
```

## 流动性指标

```python
for t in range(13,len(WeekData_factor2)):
    if WeekData_factor2['M2'][t] > (np.percentile(np.array([WeekData_factor2['M2'][t-12:t]]),62)):
        Signal_factor2[t] = 1
        loc = t
    elif WeekData_factor2['M2'][t] < (np.percentile(np.array([WeekData_factor2['M2'][t-12:t]]),62)):
        Signal_factor2[t] = -1
    else:
        Signal_factor2[t] = Signal_factor2[t-1]
```

## 情绪指标

```python
for t in range(1,len(WeekData_factor3)):
    if WeekData_factor3['CFTC'][t] > (np.percentile(np.array([WeekData_factor3['CFTC'][0:t]]),98)):
        Signal_factor3[t] = 1
        loc = t
    elif WeekData_factor3['CFTC'][t] < (np.percentile(np.array([WeekData_factor3['CFTC'][0:t]]),98)):
        Signal_factor3[t] = -1
    else:
        Signal_factor3[t] = Signal_factor3[t-1]
```

## 美元指数

```python
for t in range(7, len(WeekData_factor4)):
    if np.mean(WeekData_factor4['USD index'][t-3:t]) < np.mean(WeekData_factor4['USD index'][t-7:t-4]):
        Signal_factor4[t] = 1
        loc = t
    elif np.mean(WeekData_factor4['USD index'][t-3:t]) > np.mean(WeekData_factor4['USD index'][t-7:t-4]):
        Signal_factor4[t] = -1
    else:
        Signal_factor4[t] = Signal_factor4[t-1]
```

## 风险因子信号

```python
for t in range(2, len(WeekData_factor5)):
    if (WeekData_factor5['VIX index'][t] < (np.percentile(np.array([WeekData_factor5['VIX index'][0:t-1]]),45)))&(WeekData_factor5['VIX index'][t] > 17):
        Signal_factor5[t] = 1
        loc = t
    elif (WeekData_factor5['VIX index'][t] > (np.percentile(np.array([WeekData_factor5['VIX index'][0:t-1]]),55)))&(WeekData_factor5['VIX index'][t] > 17):
        Signal_factor5[t] = -1
    else:
        Signal_factor5[t] = 0
```


# 过程记录
## 对问题的记录

### 2022/06/29
1. 时间频率不太对，可能需要resample，研报中给的可能是周数据，实际上使用的是月数据。
2. 「已修正」因子3的观测窗口区间不太对，需要重新考虑一下，当前采用的是全部数据的70分位数，这样会导致设置规则之后，前半部分因为不符合相应的规则而不交易。如果降低分位数会导致整个交易的曲线下滑，最终的结果反而不如修改之前。

### 2022/06/30
1. 发现了一个很严重的问题，跟6.29的还是同一个问题，就是时间频率的问题。

### 2022/07/01
1. 2022年过一半了qwq，然而我雅思还没考成
2. 修复了前两天的问题，今天吧所有因子都写完了。


## 对问题的修正

### 2022/06/29
1. 关于因子3的观测窗口区间的问题，重新采取了一个新的措施，就是根据时间的长短来设定观测窗口，比如说，t=10时，则观测窗口为前10个时间点的数据的分位数，这样显得稍微合理一些。毕竟从人之常情来看过去的时间点不能预测未来的数据。修正之后，结果显得稍微比较合理（注：这里仍然使用的是月数据而不是周数据）左：修改因子3规则前的表现  右：修改因子3规则后的表现：

<div align=center><img src="https://github.com/muzian666/Quantitative-Analysis-of-Commodities/blob/main/2022.06.29/Result/Factor3-2022.06.29.png" width="350px" alt="修改之前的因子3表现"><img src="https://github.com/muzian666/Quantitative-Analysis-of-Commodities/blob/main/2022.06.29-1/Result/Factor3-2022.06.29.png" width="350px" alt="修改之后的因子3表现"></div>

可以看出，修改了因子3的规则后，其中前半段会开始进行投资了，但是综合表现却不如修改前，虽然但是，修改之后会使得投资表现的更加合理。

修改前代码（为了代码清晰，所以把规则和求分位数的部分给分开了「实际上就是我自己已经弄混了」）：

```python
Motion_Array = np.array([MonthlyData_Factor3['Motion']])
Motion_Array = Motion_Array.astype('float')
Percentile_Motion = np.percentile(Motion_Array,70)
Signal_factor_3 = pd.Series(index = time_factor_3, data = 0)
loc = 0
for t in range(1,len(MonthlyData_Factor3)):
    if (Signal_factor_3[t-1]!=1)&((MonthlyData_Factor3['Motion'][t-1])>Percentile_Motion):
        Signal_factor_3[t] = 1
        loc = t
    elif (Signal_factor_3[t-1]!=0)&((MonthlyData_Factor3['Motion'][t-1])<Percentile_Motion):
        Signal_factor_3[t] = -1
    else:
        Signal_factor_3[t] = Signal_factor_3[t-1]
```

修改后代码（为了防止代码累赘，所以把规则和求分位数的部分放在一起了「实际上就是后面我想了半天之后把逻辑给理顺了，然后放在一起写了」）：

```python
for t in range(1,len(MonthlyData_Factor3)):
    if (Signal_factor_3[t-1]!=1)&((MonthlyData_Factor3['Motion'][t-1])<(np.percentile(np.array([MonthlyData_Factor3['Motion'][0:t]]),60))):
        Signal_factor_3[t] = 1
        loc = t
    elif (Signal_factor_3[t-1]!=0)&((MonthlyData_Factor3['Motion'][t-1])>(np.percentile(np.array([MonthlyData_Factor3['Motion'][0:t]]),60))):
        Signal_factor_3[t] = -1
    else:
        Signal_factor_3[t] = Signal_factor_3[t-1]
```

### 2022/06/30
1. 没能在原有的基础上进行修改，推翻重来了QwQ
2. 写完了第一个因子：库存因子
3. 定义了一个全局变量Price，定义全局变量的原因是因为被研报前面的几句话给坑了，以为用的是OPEC价格，没想到全篇用的都是NYMEX价格，之前没注意。。。真的有被谢到。Price定义代码如下：
```python
price = pd.DataFrame(pd.read_csv('./WeekData/NYMEX.csv', encoding = 'utf-8', header = None))
price = price.iloc[1:1776,:]
price.columns = ['date', 'price']
price = price.set_index('date')
price = price['2009-12-25':'2021']
price = price.astype('float')
price_return = price/price.shift(1)-1
```

这里顺便就把Price的return给计算了，反之后面能全部用上。

4. 因为美国炼厂开工率在Wind上没有，同花顺iFinD Mac上安装不了，所以拜托了大哥帮我找了月度数据，不太好意思麻烦人家，所以就resample了一下，resample的代码如下：
```python
factor1_2 = factor1_2.iloc[1:261,:]
factor1_2 = factor1_2.iloc[:,1]
factor1_2 = factor1_2.astype('float')
factor1_2.index = pd.period_range('31/10/2000', freq='M', periods=260)
factor1_2 = factor1_2.resample('W', convention='end').asfreq()
factor1_2 = factor1_2.interpolate()
```

5. 出来的结果跟之前差不多，可能数据频率并不会对整体趋势造成影响，所以修改了一下买空买入的条件，修改之后表现还可以。

修改前：

```python
for t in range(1,len(MonthlyData_factor1)):
    if (Signal_factor1[t-1]!=1)&((stock_change[t]>stock_change[t-1])):
        Signal_factor1[t] = 1
        loc = t
    elif (Signal_factor1[t-1]!=0)&((stock_change[t]<stock_change[t-1])):
        Signal_factor1[t] = 0
    else:
        Signal_factor1[t] = Signal_factor1[t-1]
```

修改后：

```python
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
```

至于后面的绝对值加减数范围是怎么得出来的，我用的是比较笨的办法，就是观察数据组，然后一个一个去试的QwQ，累死了。

### 2022/07/01
1. 好烦啊，怎么2022年就过了一半了呢，真让人头大
2. 今天把所有的因子都写完了，其中有几个因子仔细的调了一下参数，效果还可以，但是跟研报展示的结果还是毫无关系。
3. 我不太能理解他们是怎么又是周数据又是月数据又是季数据的，这样数据也没法对齐啊，到底是怎么做到的，我非常的好奇。
4. Whatever 不管了，所有的内容都已经写完了，下周去跟大大哥讨论一下详细的内容。

### 2022/07/04
1. 可恶，发现数据出现了问题，开始对数据进行一定的修改。
2. 发现sharp ratio太高了，这说明风险值也很高，不具备实际可操作性，修改一下～

## 结果展示
### 2022/06/29

左：综合因子相对于基准表现   右：所有因子相对于基准的表现

<div align=center><img src="https://github.com/muzian666/Quantitative-Analysis-of-Commodities/blob/main/2022.06.29-1/Result/FactorF-2022.06.29.png" width = "350px" alt="单个综合因子展现"><img src="https://github.com/muzian666/Quantitative-Analysis-of-Commodities/blob/main/2022.06.29-1/Result/FactorT-2022.06.29.png" width="350px" alt="所有因子表现"></div>

### 2022/06/30

hh，没啥实际上的结果，今天只完成了对因子1的重新修改，放一张效果最好的图和之前结果的对比吧QwQ

<div align=center><img src="https://github.com/muzian666/Quantitative-Analysis-of-Commodities/blob/main/2022.06.29-1/Result/Factor1-2022.06.29.png" width = "350px" alt="因子1-旧"><img src="https://github.com/muzian666/Quantitative-Analysis-of-Commodities/blob/main/2022.06.30/Result/Factor%201.png" width = "350px" alt="因子1重新调参"></div>




