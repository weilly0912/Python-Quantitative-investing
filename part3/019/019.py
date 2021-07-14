'''
#Please use the following example commands to specify the path containing code and data:
import os
os.chdir('E:\\PythonBook_code_data\\part3\\019')

'''
import pandas as pd
stock=pd.read_csv('2330.csv',index_col='Date',sep='\t')
stock.head()

close=stock.Close 
close.index=pd.to_datetime(close.index)


lagclose=close.shift(1)
lagclose.head()


simpleret=(close-lagclose)/lagclose
simpleret.name='simpleret'
simpleret.head()


simpleret2=(close-close.shift(2))/close.shift(2)
simpleret2.name='simpleret2'
simpleret2.head()



import ffn
ffnSimpleret=ffn.to_returns(close)
ffnSimpleret.name='ffnSimpleret'
ffnSimpleret.head()


annualize=(1+simpleret).cumprod()[-1]**(245/311)-1
annualize

def annualize(returns,period):
    if period=='day':
        return((1+returns).cumprod()[-1]**(245/len(returns))-1)
    elif period=='month':
        return((1+returns).cumprod()[-1]**(12/len(returns))-1)
    elif period=='quarter':
        return((1+returns).cumprod()[-1]**(4/len(returns))-1)
    elif period=='year':
        return((1+returns).cumprod()[-1]**(1/len(returns))-1)
    else:
        raise Exception("Wrong period")

import numpy as np
comporet=np.log(close/lagclose)
comporet.name='comporet'
comporet.head()

ffnComporet=ffn.to_log_returns(close)
ffnComporet.head()

comporet2=np.log(close/close.shift(2))
comporet2.name='comporet2'
comporet2.head()


comporet2=comporet2.dropna()
comporet2.head()

sumcomporet=comporet+comporet.shift(1)
sumcomporet.head()

import matplotlib.pyplot as plt
plt.plot(simpleret)
plt.title('台積電收盤價的單期收益率')
plt.show()

cumRet=(1+simpleret).cumprod()-1
plt.plot(cumRet)
plt.title('台積電收盤價的累積收益率')
plt.show()




TSMC=pd.read_csv('2330.csv',sep='\t',index_col='Date')
TSMC.index=pd.to_datetime(TSMC.index)

FoxConn=pd.read_csv('2317.csv',sep='\t',index_col='Date')
FoxConn.index=pd.to_datetime(FoxConn.index)

retTSMC=ffn.to_returns(TSMC.Close).dropna()
retFoxConn=ffn.to_returns(FoxConn.Close).dropna()

retTSMC.std()
retFoxConn.std()

def cal_half_dev(returns):
    mu=returns.mean()
    temp=returns[returns<mu]
    half_deviation=(sum((mu-temp)**2)/len(returns))**0.5
    return(half_deviation)

cal_half_dev(retTSMC)
cal_half_dev(retFoxConn)


retTSMC.quantile(0.05)
retFoxConn.quantile(0.05)


from scipy.stats import norm
norm.ppf(0.05,retTSMC.mean(),retTSMC.std())
norm.ppf(0.05,retFoxConn.mean(),retFoxConn.std())


retTSMC[retTSMC<=retTSMC.quantile(0.05)].mean()
retFoxConn[retFoxConn<=retFoxConn.quantile(0.05)].mean()

import datetime
r=pd.Series([0,0.1,-0.1,-0.01,0.01,0.02],index=[datetime.date(2015,7,x) for x in range(3,9)])
r
value=(1+r).cumprod()
value
D=value.cummax()-value
D
d=D/(D+value)
d
MDD=D.max()
MDD
mdd=d.max()
mdd
ffn.calc_max_drawdown(value)
ffn.calc_max_drawdown((1+retTSMC).cumprod())
ffn.calc_max_drawdown((1+retFoxConn).cumprod())