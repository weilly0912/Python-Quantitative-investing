'''
#Please use the following example commands to specify the path containing code and data:
import os
os.chdir('E:\\PythonBook_code_data\\part5\\29')
'''
import pandas as pd
import matplotlib.pyplot as plt

Foxconn=pd.read_csv('2317.csv',sep='\t')
Foxconn.index=pd.to_datetime(Foxconn.Date,
              format='%Y-%m-%d')
Foxconn.head(2)

Close=Foxconn.Close
Close.describe()

lag5Close=Close.shift(5)

momentum5=Close-lag5Close
momentum5.tail()


#plot
#plt.rcParams['font.sans-serif'] = ['SimHei']
plt.subplot(211)
plt.plot(Close['2016-08-01':'2016-12-31'],'b*')
plt.xlabel('date')
plt.ylabel('Close')
plt.title('鴻海股價5日動量圖')

plt.subplot(212)
plt.plot(momentum5['2016-08-01':'2016-12-31'],'r-*')
plt.xlabel('date')
plt.ylabel('Momentum5')
plt.show()

#divide
Momen5=Close/lag5Close-1
Momen5=Momen5.dropna();
Momen5[:5]


#momentum function
def momentum(price,periond):
    lagPrice=price.shift(periond)
    momen=price-lagPrice
    momen= momen.dropna()
    return(momen)

momentum(Close,5).tail(n=5)


momen35=momentum(Close,35)

import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter, WeekdayLocator, \
                                DayLocator, MONDAY, date2num
from matplotlib.finance import candlestick_ohlc
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False


def candleLinePlots(candleData, candleTitle='a', **kwargs):
    Date = [date2num(date) for date in candleData.index]
    candleData.loc[:,'Date'] = Date
    listData = []    
    for i in range(len(candleData)):
        a = [candleData.Date[i],\
            candleData.Open[i],candleData.High[i],\
            candleData.Low[i],candleData.Close[i]]
        listData.append(a)
    # 如 果 不 定 長 參 數 無 取 值 ， 只 畫 蠟 燭 圖
    ax = plt.subplot()
    
    # 如 果 不 定 長 參 數 有 值 ， 則 分 成 兩 個 子 圖
    flag=0
    if kwargs:
        if kwargs['splitFigures']:
            ax = plt.subplot(211)
            ax2= plt.subplot(212)
            flag=1;
        # 如 果 無 參 數 splitFigures ， 則 只 畫 一 個 圖 形 框
        # 如 果 有 參 數 splitFigures ， 則 畫 出 兩 個 圖 形 框        
        for key in kwargs:
            if key=='title':
                ax2.set_title(kwargs[key])
            if key=='ylabel':
                ax2.set_ylabel(kwargs[key])
            if key=='grid':
                ax2.grid(kwargs[key])
            if key=='Data':
                plt.sca(ax)
                if flag:
                    plt.sca(ax2)
                    
                #一維數據
                if kwargs[key].ndim==1:
                    plt.plot(kwargs[key],\
                             color='k',\
                             label=kwargs[key].name)
                    plt.legend(loc='best')
                #二維數據有兩個columns
                elif all([kwargs[key].ndim==2,\
                          len(kwargs[key].columns)==2]):
                    plt.plot(kwargs[key].iloc[:,0], color='k', 
                             label=kwargs[key].iloc[:,0].name)
                    plt.plot(kwargs[key].iloc[:,1],\
                             linestyle='dashed',\
                             label=kwargs[key].iloc[:,1].name)
                    plt.legend(loc='best')
    
    mondays = WeekdayLocator(MONDAY)
    weekFormatter = DateFormatter('%y %b %d')
    ax.xaxis.set_major_locator(mondays)
    ax.xaxis.set_minor_locator(DayLocator())
    ax.xaxis.set_major_formatter(weekFormatter)
    plt.sca(ax)
    
    candlestick_ohlc(ax,listData, width=0.7,\
                     colorup='r',colordown='g')
    ax.set_title(candleTitle)
    plt.setp(ax.get_xticklabels(),\
             rotation=20,\
             horizontalalignment='center')
    ax.autoscale_view()   
    return(plt.show())
                



#candle 模組是本書編的模組，裡面有繪製K線函數candleLinePlots
import candle
Foxconn15=Foxconn['2015']
candle.candleLinePlots(Foxconn15,\
               candleTitle='鴻海股票2015年日K線圖',\
               splitFigures=True,Data=momen35['2015'],\
               title='35日動量',ylabel='35日動量')



Close=Foxconn.Close
momen35=momentum(Close,35)
momen35.head()

signal=[1 if momen35Value>0 else -1 for momen35Value in momen35]
signal=pd.Series(signal,index=momen35.index)
signal.head()

tradeSig = signal.shift(1)
ret=Close/Close.shift(1)-1
Mom35Ret=(ret*(signal.shift(1))).dropna()
Mom35Ret[:5]

win=Mom35Ret[Mom35Ret>0]
winrate=len(win)/len(Mom35Ret)
winrate


plt.subplot(2,1,1)
plt.plot(ret[Mom35Ret.index],'b')
plt.ylabel('return')
plt.title('鴻海收益率時序圖')

plt.subplot(2,1,2)
plt.plot(Mom35Ret,'r')
plt.ylabel('Mom35Ret')
plt.title('鴻海動量交易收益率時序圖')
plt.show()


loss=-Mom35Ret[Mom35Ret<0]

plt.subplot(2,1,1)
win.hist()
plt.title("盈利直方圖")
plt.subplot(2,1,2)
loss.hist()
plt.title("損失直方圖")
plt.show()

performance=pd.DataFrame({"win":win.describe(),\
"loss":loss.describe()})

performance