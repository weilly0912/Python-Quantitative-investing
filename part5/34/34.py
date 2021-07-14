'''
#Please use the following example commands to specify the path containing code and data:
import os
os.chdir('E:\\PythonBook_code_data\\part5\\34')
'''

import pandas as pd
import numpy as np
WeiChuan=pd.read_csv('1201.csv',sep='\t',
           index_col='Date')
WeiChuan.index=pd.to_datetime(WeiChuan.index)
WeiChuan.head()

from candle import candleVolume
#price up, volume up 
candleVolume(WeiChuan['2014-07'],
            candletitle='味全2014年7月份蠟燭圖',
             bartitle='味全2014年7月份日成交量')

# up,ping
WeiChuan2=WeiChuan['2014-12':'2015-01']
candleVolume(WeiChuan2,candletitle='味全2014年12月和2015年1月份蠟燭圖',\
            bartitle='味全2014年12月和2015年1月份日成交量')

# up,down
candleVolume(WeiChuan['2014-02'],
            candletitle='味全2014年2月份蠟燭圖',\
            bartitle='味全2014年2月份日成交量')

# ping up   
candleVolume(WeiChuan['2014-08'],
          candletitle='味全2014年8月份蠟燭圖',\
            bartitle='味全2014年8月份日成交量')

# ping down
candleVolume(WeiChuan['2014-03'],
             candletitle='味全2014年3月份蠟燭圖',\
             bartitle='味全2014年3月份日成交量')

# down up 
candleVolume(WeiChuan['2014-01-01':'2014-03-31'],
            candletitle='味全2014年前三個月蠟燭圖',\
            bartitle='味全2014年前三個月日成交量')

# down ping 14-01
candleVolume(WeiChuan['2014-01'],
            candletitle='味全2014年1月份蠟燭圖',\
            bartitle='味全2014年1月份日成交量')

# down down 14-02
candleVolume(WeiChuan['2014-02'],
            candletitle='味全2014年2月份蠟燭圖',\
            bartitle='味全2014年2月份日成交量')

###bar plot 
close=WeiChuan.Close
close.describe()
BreakClose=np.ceil(close/3)*3
BreakClose.name='BreakClose'
pd.DataFrame({'BreakClose':BreakClose,\
            'Close':close}).head(n=2)

volume=WeiChuan.Volume
PrcChange=close.diff()

UpVol=volume.replace(volume[PrcChange<0],0)
UpVol[0]=0

DownVol=volume.replace(volume[PrcChange>=0],0)
DownVol[0]=0

def VOblock(vol,BreakClose=BreakClose):
    return([np.sum(vol[BreakClose==x]) for x in np.unique(BreakClose)])

cumUpVol=VOblock(UpVol)
cumDownVol=VOblock(DownVol)
ALLVol=np.array([cumUpVol,cumDownVol]).transpose()

import matplotlib.pyplot as plt
fig,ax=plt.subplots()
ax1=ax.twiny()
ax.plot(close)
ax.set_title('不同價格區間的累積成交量圖')
ax.set_ylabel('價格')
ax.set_ylim(16,52)
ax.set_xlabel('時間')
plt.setp(ax.get_xticklabels(),
         rotation=20,horizontalalignment='center')
ax1.barh(bottom=range(16,52,3),width=ALLVol[:,0],\
         height=3,color='g',alpha=0.2)
ax1.barh(bottom=range(16,52,3),width=ALLVol[:,1],height=3,
        left=ALLVol[:,0],\
        color='r',alpha=0.2)
plt.show()

### strategy 
volume=WeiChuan.Volume
VolSMA5=pd.rolling_apply(volume,5,np.mean).dropna()
VolSMA10=pd.rolling_apply(volume,10,np.mean).dropna()
VolSMA=((VolSMA5+VolSMA10)/2).dropna()
VolSMA.head(n=3)

VolSignal=(volume[-len(VolSMA):]>VolSMA)*1
VolSignal[VolSignal==0]=-1
VolSignal.head()

close=WeiChuan.Close
PrcSMA5=pd.rolling_apply(close,5,np.mean).dropna()
PrcSMA12=pd.rolling_apply(close,12,np.mean).dropna()

def upbreak(Line,RefLine):
    signal=np.all([Line>RefLine,Line.shift(1)<RefLine.shift(1)],axis=0)
    return(pd.Series(signal[1:],index=Line.index[1:]))

def downbreak(Line,RefLine):
    signal=np.all([Line<RefLine,Line.shift(1)>RefLine.shift(1)],axis=0)
    return(pd.Series(signal[1:],index=Line.index[1:]))

UpSMA=upbreak(PrcSMA5[-len(PrcSMA12):],PrcSMA12)*1
DownSMA=downbreak(PrcSMA5[-len(PrcSMA12):],PrcSMA12)*(-1)
SMAsignal=UpSMA+DownSMA
VolSignal=VolSignal[-len(SMAsignal):]
signal=VolSignal+SMAsignal
signal.describe()

trade=signal.replace([2,-2,1,-1,0],[1,-1,0,0,0])
trade=trade.shift(1).dropna()
trade.head()


def TradeSim(price,signal,initial=200000):
    share=pd.Series(np.zeros(len(signal)),index=price.index)
    cash=initial*np.ones(len(signal))
    for i in range(1,len(signal)):
        cash[i] = cash[i-1]
        share[i] = share[i-1]
        case1 = (share[i]>=5000)&(signal[i] ==-1)
        case2 =(share[i]<=-5000)&(signal[i] ==1)
        case3 = (signal[i]!=0)&(abs(share[i])<5000)
        if any([case1,case2,case3]):
            cash[i] -= signal[i]*price[i]*1000
            share[i] += signal[i]*1000
    asset=cash+price*share
    asset.name='asset'
    account=pd.DataFrame({'asset':asset,'cash':cash,'share':share})
    return(account)


TradeAccount=TradeSim(close[trade.index],trade)
TradeAccount.tail()

TradeAccount.plot(subplots=True,\
        title='味全量價關係策略交易賬戶表現')
plt.show()