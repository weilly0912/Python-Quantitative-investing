'''
Please use the following example commands to specify the path containing code and data:
import os
os.chdir('E:\\PythonBook_code_data\\part5\\31')
'''

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

TSMC=pd.read_csv('2330.csv',sep='\t')
TSMC.index=pd.to_datetime(TSMC.Date)
TSMC.head(n=3)

Close=TSMC.Close
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.plot(Close,'k')
plt.xlabel('Date')
plt.ylabel('Close')
plt.title('台積電股票收盤價時序圖')

#### SMA
Sma5=pd.Series(0.0,index=Close.index)

for i in range(4,len(Close)):
    Sma5[i]=np.mean(Close[(i-4):(i+1)])

Sma5.tail()


plt.plot(Close[4:],label="Close",color='g')
plt.plot(Sma5[4:],label="Sma5",color='r',linestyle='dashed')
plt.title("台積電收盤價與簡單移動平均線图")
plt.legend()

def smaCal(tsPrice,k):
    sma=pd.Series([np.nan]*len(tsPrice),index=tsPrice.index)
    for i in range(k-1,len(tsPrice)):
        sma[i]=np.mean(tsPrice[(i-k+1):(i+1)])
    return(sma)

sma5=smaCal(Close ,5)    
sma5.head()
 
def smaCal_gene(price,k):
    #priceList只存需要計算的k期股價數據
    #用first in first out的方式來存刪數據，進而體現移動的思想
    priceList=[]
    n = len(price)
    for i in range(n):
        #在priceList中增加最新一筆數據
        priceList.append(price[i])
        if len(priceList)==k:
            yield np.mean(priceList)
            #刪除priceList中第0期數據
            priceList.pop(0)

sma5_generator = smaCal_gene(Close ,5)
next(sma5_generator)

##WMA 
b=np.array([1,2,3,4,5])
w=b/sum(b)
w

m1Close=Close[:5]
wec=w*m1Close
sum(wec)


Wma5=pd.Series([np.nan]*len(Close),index=Close.index)

for i in range(4,len(Close)):
    Wma5[i]=np.sum(w*Close[(i-4):(i+1)])

Wma5[2:7]


plt.plot(Close[4:],label="Close",color='g')
plt.plot(Wma5[4:],label="Wma5",color='r',linestyle='dashed')
plt.title('台積電收盤價加權移動平均線')
plt.legend()

def wmaCal(tsPrice,weight):
    k=len(weight)
    arrWeight=np.array(weight)
    Wma=pd.Series([np.nan]*len(tsPrice),index=tsPrice.index)
    for i in range(k-1,len(tsPrice.index)):
        Wma[i]=sum(arrWeight*tsPrice[(i-k+1):(i+1)])
    return(Wma)

wma5=wmaCal(Close,w)   
wma5.head()
   
wma5=wmaCal(Close,[0.1,0.15,0.2,0.25,0.3])
wma5.tail()

def wmaCal_gene(price,w):
    #priceList只存需要計算的k期股價數據
    #用first in first out的方式來存刪數據，進而體現移動的思想
    priceList=[]
    n = len(price)
    w=np.array(w)
    k=len(w)
    for i in range(n):
        #在priceList中增加最新一筆數據
        priceList.append(price[i])
        if len(priceList)==k:
            yield np.sum(np.array(priceList)*w)
            #刪除priceList中第0期數據
            priceList.pop(0)
            
wma5_generator=wmaCal_gene(Close,w) 
next(wma5_generator)

Ewma5=pd.Series([np.nan]*len(Close),index=Close.index)
Ewma5[4]=np.mean(Close[:4])
for i in range(5,len(Close)):
    Ewma5[i]=0.2*Close[i]+(1-0.2)*Ewma5[i-1]

Ewma5.tail()

#plt.rcParams['font.sans-serif'] = ['SimHei']
plt.plot(Close[4:],label="Close",color='k')
plt.plot(Ewma5[4:],label="Ewma5",\
         color='g',linestyle='-.')
plt.title('台積電收盤價指數加權移動平均線')
plt.legend()


def ewmaCal(tsprice,period=5,exponential=0.2):
   Ewma=pd.Series([np.nan]*len(tsprice),index=tsprice.index)
   Ewma[period-1]=np.mean(tsprice[:period])
   for i in range(period,len(tsprice)):
       Ewma[i]=exponential*tsprice[i]+(1-exponential)*Ewma[i-1]
   return(Ewma)

Ewma=ewmaCal(Close,5,0.2)
Ewma.tail()

def ewmaCal_gene(price,k,e):
    for i in range(k-1,len(price)):
        if i==k-1:
            ewmaValue=np.mean(price[:k])
        else:
            ewmaValue=e*price[i]+(1-e)*ewmaValue
        yield ewmaValue

ewma_generator=ewmaCal_gene(Close,5,0.2)
next(ewma_generator)
next(ewma_generator)


import movingAverage as ma
Ewma10=ma.ewmaCal(Close,10,0.2)
Ewma10.tail(n=3)


#TSMC
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import movingAverage as ma
TSMC=pd.read_csv('2330.csv',sep='\t')
TSMC.index=pd.to_datetime(TSMC.Date)
Close=TSMC.Close
Close.describe()

Close15=Close['2015']

sma10=ma.smaCal(Close15,10)
sma10.tail(n=3)

weight=np.array(range(1,11))/sum(range(1,11))
wma10=ma.wmaCal(Close15,weight)
wma10.tail(n=3)

expo= 2/(len(Close15)+1)
ewma10=ma.ewmaCal(Close15,10,expo)
ewma10.tail(n=3)


plt.plot(Close15[10:],label="Close",color='k')
plt.plot(sma10[10:],label="sma10",color='r',linestyle='dashed')
plt.plot(wma10[10:],label="wma10",color='b',linestyle=':')
plt.plot(ewma10[10:],label="ewma10",color='G',linestyle='-.')
plt.title('台積電股價和三種均線圖')
plt.legend()

sma5=ma.smaCal(Close15,5)
sma30=ma.smaCal(Close15,30)
plt.plot(Close15[30:],label="Close",color='k')
plt.plot(sma5[30:],label="sma5",color='b',linestyle='dashed')
plt.plot(sma30[30:],label="sma30",color='r',linestyle=':')
plt.title("台積電股票價格的長短期均線")
plt.legend()


#trading-sma10 and close
sma10_gene=ma.smaCal_gene(Close,10)
sma10_before = next(sma10_gene)
smaSignal=[]
for i in range(11,len(Close)):
    sma10_now = next(sma10_gene)
    if Close[i-1]<sma10_before and Close[i]>sma10_now:
        smaSignal.append(1)
    elif Close[i-1]>sma10_before and Close[i]<sma10_now:
        smaSignal.append(-1)
    else:
        smaSignal.append(0)
    sma10_before = sma10_now
    

smaSignal=pd.Series(smaSignal,index=Close.index[11:])

smaTrade=smaSignal.shift(1).dropna()
smaBuy=smaTrade[smaTrade==1]
smaBuy.head(n=3)
smaSell=smaTrade[smaTrade==-1]
smaSell.head(n=3)

tsmcRet=Close/Close.shift(1)-1
smaRet=(tsmcRet*smaTrade).dropna()

cumStock=np.cumprod(1+tsmcRet[smaRet.index[0]:])-1
cumTrade=np.cumprod(1+smaRet)-1
cumdata=pd.DataFrame({'cumTrade':cumTrade,\
                     'cumStock':cumStock})
cumdata.iloc[-6:,:]

plt.plot(cumStock,label="cumStock",color='k')
plt.plot(cumTrade,label="cumTrade",color='r',linestyle=':')
plt.title('股票本身與均線交易的累積收益率')
plt.legend()

smaRet[smaRet==(-0)]=0
smaWinrate=len(smaRet[smaRet>0])/len(smaRet[smaRet!=0])
smaWinrate

#short  and  long
sma5_gene=ma.smaCal_gene(Close,5)
sma30_gene=ma.smaCal_gene(Close,30)
sma5_before = next(sma5_gene)
sma30_before = next(sma30_gene)
SLSignal=[]
for i in range(31,len(Close)):
    sma5_now = next(sma5_gene)
    sma30_now = next(sma30_gene)
    if sma5_before<sma30_before and sma5_now>sma30_now:
        SLSignal.append(1)
    elif sma5_before>sma30_before and sma5_now<sma30_now:
        SLSignal.append(-1)
    else:
        SLSignal.append(0)
    sma5_before = sma5_now
    sma30_before = sma30_now

SLSignal = pd.Series(SLSignal,index = Close.index[31:])
SLSignal[SLSignal==1]
SLSignal[SLSignal==-1]

SLTrade=SLSignal.shift(1)

Long=pd.Series(0,index=SLTrade.index)
Long[SLTrade==1]=1
LongRet=(Long*tsmcRet).dropna()
winLrate=len(LongRet[LongRet>0])/len(LongRet[LongRet!= 0] )
winLrate

Short= pd.Series(0,index=SLTrade.index)
Short[SLTrade==-1]=-1
ShortRet=(Short*tsmcRet).dropna()
winSrate=len(ShortRet[ShortRet>0])/len(ShortRet[ShortRet!=0])
winSrate

SLtradeRet=(SLTrade*tsmcRet).dropna()
winRate= len(SLtradeRet[SLtradeRet>0])/len(\
         SLtradeRet[SLtradeRet!=0])
winRate

cumLong=np.cumprod(1+LongRet)-1
cumShort=np.cumprod(1+ShortRet)-1
cumSLtrade=np.cumprod(1+SLtradeRet)-1

plt.plot(cumSLtrade,label="cumLong&Short",color='k')
plt.plot(cumLong, label="cumLong",\
         color='b',linestyle='dashed')
plt.plot(cumShort,label="cumShort",\
         color='r',linestyle=':')
plt.title('長短期均線交易累積收益率')
plt.legend(loc='best')

#MACD
DIF=ma.ewmaCal(Close,12,2/(1+12))\
       -ma.ewmaCal(Close,26,2/(1+26))
DIF.tail(n=3)

DEA=ma.ewmaCal(DIF.dropna(),9,2/(1+9))
DEA.tail()

MACD=DIF-DEA
MACD.tail(n=3)

plt.subplot(211)
plt.plot(DIF['2016-12'],\
      label="DIF",color='k')
plt.plot(DEA['2016-12'], label="DEA",\
        color='b',linestyle='dashed')
plt.title('信號線DIF与DEA')
plt.legend()
plt.subplot(212)
plt.bar(left=MACD['2016-12'].index,\
        height=MACD['2016-12'],\
        label='MACD',color='r')
plt.title('柱狀圖MACD')
plt.legend()

macddata=pd.DataFrame()
macddata['DIF']= DIF['2016-08':'2016-12']
macddata['DEA']= DEA['2016-08':'2016-12']
macddata['MACD']= MACD['2016-08':'2016-12']

import candle
candle.candleLinePlots(TSMC['2016-08':'2016-12'],\
              candleTitle='台積電2016年8月到12月份的日K線圖',\
              splitFigures=True,Data=macddata,\
              ylabel='MACD')

DEA=DEA.dropna()
DIF=DIF[DEA.index]
macdSignal=pd.Series(0,index=DIF.index)
for i in range(1,len(DIF)):
    if all([DIF[i]>DEA[i]>0.0,DIF[i-1]<DEA[i-1]]):
        macdSignal[i]=1
    elif all([DIF[i]<DEA[i]<0.0,DIF[i-1]>DEA[i-1]]):
        macdSignal[i]=-1
macdSignal.tail()

macdTrade=macdSignal.shift(1)
macdRet=(tsmcRet*macdTrade).dropna()
macdRet[macdRet==-0]=0
macdWinRate=len(macdRet[macdRet>0])/len(macdRet[macdRet!=0])
macdWinRate


AllSignal=smaSignal+SLSignal+macdSignal

for i in AllSignal.index:
    if AllSignal[i]>1:
        AllSignal[i]=1
    elif AllSignal[i]<-1:
        AllSignal[i]=-1
    else:
        AllSignal[i]=0

AllSignal[AllSignal==1]
AllSignal[AllSignal==-1]

tradSig=AllSignal.shift(1).dropna()

Close=Close[-len(tradSig):]
cash=pd.Series(0.0,index=Close.index)
share=pd.Series(0,index=Close.index)

#當價格連續兩天上升且交易信號沒有顯示賣出時，
#第一次開賬戶持有股票

entry=3
cash[:entry]=1000000
while entry<len(Close):
    cash[entry]=cash[entry-1]
    if all([Close[entry-1]>=Close[entry-2],\
            Close[entry-2]>=Close[entry-3],\
            AllSignal[entry-1]!=-1]):
        share[entry]=1000
        cash[entry]= cash[entry]-1000*Close[entry]
        break
    entry+=1

#根據交易信號交易股票
i=entry+1
while i<len(tradSig):
    cash[i]=cash[i-1]
    share[i]=share[i-1]
    #買入時，買入3000share
    if tradSig[i]==1:
        share[i] = share[i]+3000
        cash[i] = cash[i]-3000*Close[i]
    #賣出時，賣出1000share
    elif tradSig[i]==-1:
        share[i] = share[i]-1000
        cash[i] = cash[i]+1000*Close[i]
    i+=1

asset=cash+share*Close

asset.tail()

plt.subplot(411)
plt.title('2015-2016年上:台積電均線交易賬戶')
plt.plot(Close, color='b')
plt.ylabel("Price")
plt.subplot(412)
plt.plot(share, color='b')
plt.ylabel("Share")
plt.ylim(0,max(share)+1000)

plt.subplot(413)
plt.plot(asset,label="asset",color='r')
plt.ylabel("Asset")
plt.ylim(min(asset)-5000,max(asset)+5000)

plt.subplot(414)
plt.plot(cash, label="cash",color='g')
plt.ylabel("Cash")
plt.ylim(min(cash)-500,max(cash)+5000)

TradeReturn=(asset[-1]-1000000)/1000000
TradeReturn
