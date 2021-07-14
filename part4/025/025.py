'''
#Please use the following example commands to specify the path containing code and data:
import os
os.chdir('E:\\PythonBook_code_data\\part4')
'''


import math
from matplotlib.font_manager import FontProperties

import numpy as np

import pandas as pd
CPI=pd.read_csv('CPI.csv',index_col='time')
CPI.index=pd.to_datetime(CPI.index)
CPI.head(n=3)
CPI.tail(n=3)
CPI.shape

CPI=CPI.sort_index()
CPItrain=CPI[:-3]
CPItrain.tail(n=3)
CPItest = CPI[-3:]
CPItest


CPI.plot(title='CPI 2001-2014')


from arch.unitroot import ADF
CPItrain=CPItrain.dropna()
print(ADF(CPItrain,max_lags=10).summary().as_text())

from statsmodels.tsa import stattools
LjungBox=stattools.q_stat(stattools.acf(CPItrain)[1:12],len(CPItrain))
LjungBox[1][-1] 


from statsmodels.graphics.tsaplots import *
import matplotlib.pyplot as plt
#將畫面一分為二
axe1=plt.subplot(121)
axe2=plt.subplot(122)
#在第一個畫面中畫出序列的自相關係數圖 
plot1=plot_acf(CPItrain,lags=30,ax=axe1)
#在第二個畫面中畫出序列的偏自相關係數圖
plot2=plot_pacf(CPItrain,lags=30,ax=axe2)

from statsmodels.tsa import arima_model
#order表示建立的模型的階數，c(1,0,1)表示建立的是ARMA(1,1)模型；
#中間的數字0表示使用原始的、未進行過差分（差分次數為0）的數據；
#此處我們無需考慮它

model1=arima_model.ARIMA(CPItrain,order=(1,0,1)).fit()
model1.summary()

#同理，我們建立起其它階數的模型
model2=arima_model.ARIMA(CPItrain,order=(1,0,2)).fit()
model2.summary()
model3=arima_model.ARIMA(CPItrain,order=(2,0,1)).fit()
model4=arima_model.ARIMA(CPItrain,order=(2,0,2)).fit()
model5=arima_model.ARIMA(CPItrain,order=(3,0,2)).fit()

model3.conf_int()
#繪製時間序列模擬的診斷圖
stdresid=model3.resid/math.sqrt(model3.sigma2)
plt.plot(stdresid)
plot_acf(stdresid,lags=20)

LjungBox=stattools.q_stat(stattools.acf(stdresid)[1:13],len(stdresid))
LjungBox[1][-1]

LjungBox=stattools.q_stat(stattools.acf(stdresid)[1:20],len(stdresid))
LjungBox[1][-1]

plot_acf(stdresid,lags=40)

model3.forecast(3)[0]
CPI.head(3)
CPItest


taisun=pd.read_csv('1218.csv',sep='\t')
taisun.index=pd.to_datetime(taisun.Date)
taisun.head()
returns=taisun.ROI['2013-01-01':'2015-01-01']
returns.head(n=3)
returns.tail(n=3)
#returns.plot()


ADF(returns).summary()


stattools.q_stat(stattools.acf(returns)[1:10],len(returns))[1]

model=arima_model.ARIMA(returns,order=(2,0,1)).fit()
model.summary()
model.conf_int()
stdresid=model.resid/math.sqrt(model.sigma2)
plt.plot(stdresid)
plot_acf(stdresid,lags=12)
LjungBox=stattools.q_stat(stattools.acf(stdresid)[1:12],len(stdresid))
LjungBox[1]
