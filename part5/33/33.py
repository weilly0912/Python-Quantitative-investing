'''
Please use the folLowing example commands to specify the path containing code and data:
import os
os.chdir('E:\\PythonBook_code_data\\part5\\33')
'''
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

GSPC=pd.read_csv('GSPC.csv',index_col='Date')
GSPC=GSPC.iloc[:,1:]
GSPC.index=pd.to_datetime(GSPC.index)
GSPC.head()

Close=GSPC.Close
High=GSPC.High
Low=GSPC.Low
ndate=len(Close)

RSV=[]
for j in range(8,ndate):
    periodHigh=np.max(High[(j-8):(j+1)])
    periodLow=np.min(Low[(j-8):(j+1)])
    RSV.append(100*(Close[j]-periodLow)\
           /(periodHigh-periodLow))

RSV=pd.Series(RSV,index=Close.index[8:])
RSV.name='RSV'
RSV.head()
RSV.describe()

Close1=Close['2015']
RSV1=RSV['2015']
Cl_RSV=pd.DataFrame([Close1,RSV1]).transpose()
Cl_RSV.plot(subplots=True,
             title='未成熟隨機指標RSV')

GSPC2015=GSPC['2015']
import candle
candle.candlePlot(GSPC2015,\
                '2015年標普500指數日K線圖')


K=[50]
D=[50]

for i in range(len(RSV)):
    KValue = (2/3)*K[-1] + (RSV[i]/3)
    DValue = (2/3)*D[-1] + KValue/3
    K.append(KValue)
    D.append(DValue)

K=pd.Series(K[1:],index=RSV.index)
K.name='KValue'
K.head()

D=pd.Series(D[1:],index=RSV.index)
D.name='DValue'
D.head()


plt.subplot(211)
plt.title('2015年標准普爾500的收盤價')
plt.plot(Close['2015'])
plt.subplot(212)
plt.title('2015年標准普爾500的RSV與KD線')
plt.plot(RSV['2015'])
plt.plot(K['2015'],linestyle='dashed')
plt.plot(D['2015'],linestyle='-.')
plt.legend(loc='upper left')

J=3*K-2*D
J.name='JValue'
J.head()

plt.subplot(211)
plt.title('2015年標准普爾500的收盤價')
plt.plot(Close['2015'])
plt.subplot(212)
plt.title('2015年標准普爾500的RSV与KDJ')
plt.plot(RSV['2015'])
plt.plot(K['2015'],linestyle='dashed')
plt.plot(D['2015'],linestyle='-.')
plt.plot(J['2015'],linestyle='--')
plt.legend(loc='upper left') 


KSignal=K.apply(lambda x:\
                    -1 if x>85 else 1 if x<20 else 0)

DSignal=D.apply(lambda x: \
                 -1 if x>80 else 1 if x<20 else 0)
KDSignal=KSignal+DSignal
KDSignal.name='KDSignal'

KDSignal[KDSignal>=1]=1
KDSignal[KDSignal<=-1]=-1
KDSignal.head(n=3)

KDSignal[KDSignal==1].head(n=3)

def trade(signal,price):
    ret=(price-price.shift(1))/price.shift(1)
    ret.name='ret'
    signal=signal.shift(1)
    tradeRet=(ret*signal).dropna()
    tradeRet.name='tradeRet'
    tradeRet[tradeRet==-0]=0
    Returns=pd.merge(pd.DataFrame(ret),\
                     pd.DataFrame(tradeRet),
                     left_index=True,\
                     right_index=True).dropna()
    return(Returns)

KDtrade=trade(KDSignal,Close)
KDtrade.rename(columns={'ret':'Ret',\
              'tradeRet':'KDtradeRet'},\
               inplace=True)
KDtrade.head()

import ffn
def backtest(ret,tradeRet):
    def performance(x):
        winpct=len(x[x>0])/len(x[x!=0])
        annRet=(1+x).cumprod()[-1]**(245/len(x))-1
        sharpe=ffn.calc_risk_return_ratio(x)
        maxDD=ffn.calc_max_drawdown((1+x).cumprod())
        perfo=pd.Series([winpct,annRet,sharpe,maxDD],\
        index=['win rate','annualized return',\
        'sharpe ratio','maximum drawdown'])
        return(perfo)
    BuyAndHold=performance(ret)
    Trade=performance(tradeRet)
    return(pd.DataFrame({ret.name:BuyAndHold,\
           tradeRet.name:Trade}))

backtest(KDtrade.Ret,KDtrade.KDtradeRet)

cumRets1=(1+KDtrade).cumprod()
plt.plot(cumRets1.Ret,label='Ret')
plt.plot(cumRets1.KDtradeRet,'--',\
          label='KDtradeRet')
plt.title('KD指標交易策略績效表現')
plt.legend()

backtest(KDtrade.Ret[:'2014-10-10'],\
          KDtrade.KDtradeRet[:'2014-10-10'])

cumRets2=(1+KDtrade[:'2014-10-10']).cumprod()
plt.plot(cumRets2.Ret,\
          label='''Ret[:'2014-10-10']''')
plt.plot(cumRets2.KDtradeRet,'--',\
          label='''KDtradeRet[:'2014-10-10']''')
plt.title('KD指標交易策略10月10日之前績效表現')
plt.legend(loc='upper left')
#plt.show()


JSignal=J.apply(lambda x:\
         -1 if x>100 else 1 if x<0 else 0)


KDJSignal=KSignal+DSignal+JSignal
KDJSignal=KDJSignal.apply(lambda x:\
          1 if x>=2 else -1 if x<=-2 else 0)

KDJtrade=trade(KDJSignal,Close)
KDJtrade.rename(columns={'ret':'Ret',\
             'tradeRet':'KDJtradeRet'},\
             inplace=True)

backtest(KDJtrade.Ret,KDJtrade.KDJtradeRet)

KDJCumRet=(1+KDJtrade).cumprod()
plt.plot(KDJCumRet.Ret,label='Ret')
plt.plot(KDJCumRet.KDJtradeRet,'--',\
          label='KDJtradeRet')
plt.title('KDJ指標交易策略績效表現')
plt.legend(loc='upper left')

backtest(KDJtrade.Ret[:'2014-10-10'],\
             KDJtrade.KDJtradeRet[:'2014-10-10'])

def upbreak(Line,RefLine):
    signal=np.all([Line>RefLine,\
                   Line.shift(1)<RefLine.shift(1)],\
                   axis=0)
    return(pd.Series(signal[1:],\
                     index=Line.index[1:]))

KDupbreak=upbreak(K,D)*1
KDupbreak[KDupbreak==1].head()

def downbreak(Line,RefLine):
    signal=np.all([Line<RefLine,\
                   Line.shift(1)>RefLine.shift(1)],\
                   axis=0)
    return(pd.Series(signal[1:],\
           index=Line.index[1:]))

KDdownbreak=downbreak(K,D)*1
KDdownbreak[KDdownbreak==1].head()

Close=Close['2014-01-14':]
difClose=Close.diff()

prctrend=2*(difClose[1:]>=0)-1
prctrend.head()

KDupSig=(KDupbreak[1:]+prctrend)==2
KDupSig.head(n=3)

KDdownSig= (KDdownbreak[1:]==1)&(prctrend==-1) 

breakSig=KDupSig*1+KDdownSig*-1
breakSig.name='breakSig'
breakSig.head()

KDbreak=trade(breakSig,Close)
KDbreak.rename(columns={'ret':'Ret',\
              'tradeRet':'KDbreakRet'},\
              inplace=True)
KDbreak.head()

backtest(KDbreak.Ret,KDbreak.KDbreakRet)

KDbreakRet=(1+KDbreak).cumprod()
plt.plot(KDbreakRet.Ret,label='Ret')
plt.plot(KDbreakRet.KDbreakRet,'--',\
          label='KDbreakRet')
plt.title('KD"金叉"與"死叉"交易策略績效表現')
plt.legend(loc='upper left')