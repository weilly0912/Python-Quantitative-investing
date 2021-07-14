'''
#Please use the following example commands to specify the path containing code and data:
import os
os.chdir('E:\\PythonBook_code_data\\part5\\28')
'''
import pandas as pd
taiex2013=pd.read_csv('taiex2013.csv',sep='\t')
taiex2013.head(n=3)

taiex2013.index = pd.to_datetime(taiex2013.Date)
type(taiex2013.index)
taiex201304 = taiex2013['2013-04'] 

from matplotlib.dates import date2num
from datetime import datetime

taiex201304.Date=[date2num(datetime.strptime(date,"%Y-%m-%d"))\
               for date in taiex201304.Date]
            
taiex201304.head()
type(taiex201304)

taiex201304_listData=[]
for i in range(len(taiex201304)):
    a=[taiex201304.Date[i],\
    taiex201304.Open[i],taiex201304.High[i],\
    taiex201304.Low[i],taiex201304.Close[i]]
    taiex201304_listData.append(a)


import numpy as np
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter, WeekdayLocator,\
    DayLocator, MONDAY
from matplotlib.finance import  candlestick_ohlc

ax= plt.subplot()
mondays = WeekdayLocator(MONDAY)
ax.xaxis.set_major_locator(mondays)
ax.xaxis.set_minor_locator(DayLocator() )
weekFormatter = DateFormatter('%y %b %d')
ax.xaxis.set_major_formatter(weekFormatter)
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False
ax.set_title('加權股價指數2013年4月份K線圖')
candlestick_ohlc(ax, taiex201304_listData, 
    width=0.7,colorup='r', colordown='g');
plt.setp(plt.gca().get_xticklabels(),
    rotation=50,
    horizontalalignment='center')
plt.show()

from candle import candlePlot

candlePlot(taiex201304,title='加權股價指數2013年4月份K線圖')

#morning star
taiex2011=pd.read_csv('taiex2011.csv',sep='\t')
taiex2011.index=pd.to_datetime(taiex2011.Date,
    format='%Y-%m-%d')

taiex2011.head(2)
taiex2011.iloc[-2:,:]

Close=taiex2011.Close
Open=taiex2011.Open
ClOp=Close-Open
ClOp.head()
ClOp.describe()

Shape = [0,0,0]
for i in range(3,len(ClOp)):
    if all([ClOp[i-2]<-20,abs(ClOp[i-1])< 20,\
    ClOp[i]>5,abs(ClOp[i])>abs(ClOp[i-2]*0.5)]):
        Shape.append(1)
    else:
        Shape.append(0)

Shape.index(1)


Doji=[0,0,0]
for i in range(3,len(Open)):
    if all([Open[i-1]<Open[i],Open[i-1]<Close[i-2],\
    Close[i-1]<Open[i],(Close[i-1]<Close[i-2])]):
        Doji.append(1)
    else:
        Doji.append(0)

Doji.count(1)


Trend=[0,0,0]
for i in range(3,len(Close)):
    if Close[i-2] < Close[i-3]:
        Trend.append(1)
    else:
        Trend.append(0)

StarSig=[]
for i in range(len(Trend)):
    if all([Shape[i]==1,Doji[i]==1,Trend[i]==1]):
        StarSig.append(1)
    else:
        StarSig.append(0)

for i in range(len(StarSig)):
    if StarSig[i]==1:
        print(taiex2011.index[i])



taiex201104=taiex2011['2011-04']


import candle
# Errata: There is an error in the book.
# the right one is as follows:
candle.candlePlot(taiex201104 ,
    title=' 加權股價指數2011年4月份的日K线图')

# Dark Cloud Cover
import pandas as pd
taiex2013=pd.read_csv('taiex2013.csv',sep ='\t')

taiex2013.index=pd.to_datetime(taiex2013.Date,
    format='%Y-%m-%d')


Close13=taiex2013.Close
Open13=taiex2013.Open


Cloud=pd.Series(0,index=Close13.index)
for i in range(1,len(Close13)):
    if all([Close13[i]<Open13[i],\
            Close13[i-1]>Open13[i-1],\
            Open13[i]>Close13[i-1],\
            Close13[i]<0.5*(Close13[i-1]+Open13[i-1]),\
            Close13[i]>Open13[i-1]]):
        Cloud[i]=1


Trend=pd.Series(0,index=Close13.index)
for i in range(2,len(Close13)):
    if Close13[i-1]>Close13[i-2]>Close13[i-3]:
        Trend[i]=1

darkCloud=Cloud+Trend
darkCloud[darkCloud==2]


taiex201304=taiex2013['2013-04']           
candle.candlePlot(taiex201304 ,\
                  title='加權股價指數2013年4月份的日K線圖')


taiex201310=taiex2013['2013-10']
candle.candlePlot(taiex201310,\
                  title='加權股價指數2013年10月份的日K線圖')


