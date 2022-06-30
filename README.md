# 大宗商品分析（原油）

是一个小白的自我学习记录，记录自己的学习过程

真的是小白，没学过py，纯纯的一边摸索一边学习一边写，写的不好，勿喷

尝试复刻研报：https://mp.weixin.qq.com/s/TW9ruRTTqupAxkvW86YZvA

数据来源：Wind金融终端、同花顺iFinD（手动摘取，没用API）

## 对问题的记录
### 2022/06/30
1. 发现了一个很严重的问题，跟6.29的还是同一个问题，就是时间频率的问题。
### 2022/06/29
1. 时间频率不太对，可能需要resample，研报中给的可能是周数据，实际上使用的是月数据。
2. 「已修正」因子3的观测窗口区间不太对，需要重新考虑一下，当前采用的是全部数据的70分位数，这样会导致设置规则之后，前半部分因为不符合相应的规则而不交易。如果降低分位数会导致整个交易的曲线下滑，最终的结果反而不如修改之前。


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

## 结果展示
### 2022/06/29

左：综合因子相对于基准表现   右：所有因子相对于基准的表现

<div align=center><img src="https://github.com/muzian666/Quantitative-Analysis-of-Commodities/blob/main/2022.06.29-1/Result/FactorF-2022.06.29.png" width = "350px" alt="单个综合因子展现"><img src="https://github.com/muzian666/Quantitative-Analysis-of-Commodities/blob/main/2022.06.29-1/Result/FactorT-2022.06.29.png" width="350px" alt="所有因子表现"></div>
