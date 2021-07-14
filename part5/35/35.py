'''
#Please use the following example commands to specify the path containing code and data:
import os
os.chdir('E:\\PythonBook_code_data\\part5\\35')
'''
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

MediaTek = pd.read_csv('2454.csv',sep='\t')
MediaTek.index = pd.to_datetime(MediaTek.Date)

close=MediaTek.Close
Volume=MediaTek.Volume

difClose=close.diff()
difClose[0]=0
OBV=(((difClose>=0)*2-1)*Volume).cumsum()
OBV.name='OBV'
OBV.head()
OBV.describe()

import movingAverage as mv
smOBV=mv.smaCal(OBV,9)
smOBV.tail()

AdjOBV=((close-MediaTek.Low)-(MediaTek.High-close)\
         )/(MediaTek.High-MediaTek.Low)*Volume
AdjOBV.name='AdjOBV'
AdjOBV.head()
AdjOBVd=AdjOBV.cumsum()
AdjOBVd.name='AdjOBVd'
AdjOBVd.describe()

ax1=plt.subplot(3,1,1)
close.plot(title='聯發科收盤價')
plt.xticks(close.index[1:3],(''))
plt.xlabel('')
ax2=plt.subplot(3,1,2)
OBV.plot(label='OBV',title='聯發科累積能量潮與移動能量潮')
smOBV.plot(label='smOBV',linestyle='-.',color='r')
plt.xlabel('')
plt.legend(loc='upper left')
plt.xticks(close.index[1:3],(''))

ax3=plt.subplot(3,1,3)
AdjOBVd.plot(title='成交量多空比率淨額')



import ffn
def trade(obv,price):
    signal=(2*(obv.diff()>0)-1)[1:]
    ret=ffn.to_returns(price)[1:]
    ret.name='ret'
    tradeRet=ret*signal.shift(1)
    tradeRet.name='tradeRet'
    Returns=pd.merge(pd.DataFrame(ret),\
                     pd.DataFrame(tradeRet),\
                    left_index=True,right_index=True).dropna()
    return(Returns)

OBVtrade=trade(OBV,close)
OBVtrade.head()

ret=OBVtrade.ret
tradeRet=OBVtrade.tradeRet
ret.name='BuyAndHold'
tradeRet.name='OBVTrade'
(1+ret).cumprod().plot(label='ret',linestyle='dashed')
(1+tradeRet).cumprod().plot(label='tradeRet')
plt.title('累積OBV交易策略績效表現')
plt.legend()

def backtest(ret,tradeRet):
    def performance(x):
        winpct=len(x[x>0])/len(x[x!=0])
        annRet=(1+x).cumprod()[-1]**(245/len(x))-1
        sharpe=ffn.calc_risk_return_ratio(x)
        maxDD=ffn.calc_max_drawdown((1+x).cumprod())
        perfo=pd.Series([winpct,annRet,sharpe,maxDD],index=['win rate',
                        'annualized return',\
                        'sharpe ratio','maximum drawdown'])
        return(perfo)
    BuyAndHold=performance(ret)
    OBVTrade=performance(tradeRet)
    return(pd.DataFrame({ret.name:BuyAndHold,\
    tradeRet.name:OBVTrade}))

OBVtest=backtest(ret,tradeRet)
OBVtest

smOBVtrade=trade(smOBV,close)
smOBVtrade.head(n=3)

ret=smOBVtrade.ret
ret.name='BuyAndHold'
smtradeRet=smOBVtrade.tradeRet
smtradeRet.name='smOBVTrade'
(1+ret).cumprod().plot(label='ret',linestyle='dashed')
(1+tradeRet).cumprod().plot(label='tradeRet')
plt.title('移動OBV交易策略績效表現')
plt.legend()

test=backtest(ret,smtradeRet)
test