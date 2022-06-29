# Quantitative-Analysis-of-Commodities
大宗商品量化分析（原油）

是一个小白的自我学习记录，记录自己的学习过程

尝试复刻研报：https://mp.weixin.qq.com/s/TW9ruRTTqupAxkvW86YZvA

## 对问题的记录
### 2022/06/29
1. 时间频率不太对，可能需要resample，研报中给的可能是周数据，实际上使用的是月数据。
2. 因子3的观测窗口区间不太对，需要重新考虑一下，当前采用的是全部数据的70分位数，这样会导致设置规则之后，前半部分因为不符合相应的规则而不交易。如果降低分位数会导致整个交易的曲线下滑，最终的结果反而不如修改之前。


## 对问题的修正
### 2022/06/29
1. 关于因子3的观测窗口区间的问题，重新采取了一个新的措施，就是根据时间的长短来设定观测窗口，比如说，t=10时，则观测窗口为前10个时间点的数据的分位数，这样显得稍微合理一些。毕竟从人之常情来看过去的时间点不能预测未来的数据。修正之后，结果显得稍微比较合理：
![如果直接使用全局观测的分位数的结果](https://github.com/muzian666/Quantitative-Analysis-of-Commodities/blob/main/2020.06.29/Result/Factor3-2022.06.29.png)
<img src="https://github.com/muzian666/Quantitative-Analysis-of-Commodities/blob/main/2020.06.29/Result/Factor3-2022.06.29.png" width="100px">



