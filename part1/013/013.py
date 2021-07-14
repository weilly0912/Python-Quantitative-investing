'''
#Please use the following example commands to specify the path containing code and data:
import os
os.chdir('E:\\PythonBook_code_data\\part1\\013')
'''
import pandas as pd
TSMC=pd.read_csv('2330stk.csv',sep='\t',index_col='Date')
TSMC.head() 
TSMC.index=pd.to_datetime(TSMC.index)
Close=TSMC.Close

import matplotlib.pyplot as plt
plt.plot(Close['2016'])


plt.plot([1,1,0,0,-1,0,1,1,-1]) 
plt.rcParams['axes.unicode_minus']=False

plt.plot([1,1,0,0,-1,0,1,1,-1])
plt.ylim(-1.5,1.5)

plt.plot([1,1,0,0,-1,0,1,1,-1])
plt.ylim(-1.5,1.5)
plt.xticks(range(9),['2015-02-01','2015-02-02','2015-02-03','2015-02-04','2015-02-05',\
'2015-02-06','2015-02-07','2015-02-08','2015-02-09'])


plt.plot([1,1,0,0,-1,0,1,1,-1])
plt.ylim(-1.5,1.5)
plt.xticks(range(9),['2015-02-01','2015-02-02','2015-02-03','2015-02-04','2015-02-05',\
'2015-02-06','2015-02-07','2015-02-08','2015-02-09'],rotation=45)

plt.plot(Close['2016'])
plt.title('台積電2016年收盤價曲線')

plt.plot(Close['2016'])
plt.title('台積電2016年收盤價曲線',loc='right') 

plt.plot(Close['2016'])
plt.title('台積電2016年收盤價曲線')
plt.xlabel('日期')
plt.ylabel('收盤價')

plt.plot(Close['2016'],label='收盤價')
plt.title('台積電2016年收盤價曲線')
plt.xlabel('日期')
plt.ylabel('收盤價')
plt.grid(True,axis='y')

Open=TSMC.Open
plt.plot(Close['2016'],label='收盤價')
plt.plot(Open['2016'],label='開盤價')
plt.legend() 

plt.plot(Close['2016'],label='收盤價',linestyle='solid')
plt.plot(Open['2016'],label='開盤價',ls='-.')
plt.legend()
plt.xlabel('日期')
plt.ylabel('價格')
plt.title('台積電2016年开盘与收盤價曲线')
plt.grid(True,axis='y')

plt.plot(Close['2016'],c='r',label='收盤價')
plt.plot(Open['2016'],c='b',ls='--',label='開盤價')
plt.legend(loc='best')
plt.xlabel('日期')
plt.ylabel('價格')# 價格
plt.title('台積電2016年开盘与收盤價曲线')
plt.grid(True,axis='both')

plt.plot(Close['2016'],marker='o',label='收盤價')
plt.plot(Open['2016'],marker='*',label='開盤價')
plt.legend(loc='best')
plt.xlabel('日期')
plt.ylabel('價格')#價格
plt.title('台積電2016年开盘与收盤價曲线')
plt.grid(True,axis='both')

plt.plot(Close['2016'],'--rD',label='收盤價')
plt.plot(Open['2016'],'--b>',label='開盤價')
plt.legend(loc='best')
plt.xlabel('日期')
plt.ylabel('價格')#價格
plt.title('台積電2016年开盘与收盤價曲线')
plt.grid(True,axis='both')

plt.plot(Close['2016'],'--rD',label='收盤價',linewidth=2)
plt.plot(Open['2016'],'--b>',label='開盤價',lw=10)
plt.legend(loc='best')
plt.xlabel('日期')
plt.ylabel('價格')
plt.title('台積電2016年开盘与收盤價曲线')
plt.grid(True,axis='both')

Close.describe()
a=[0,0,0]
for i in Close:
    if i>180:
        a[2]+=1
    elif i>150:
        a[1]+=1
    else:
        a[0]+=1
a    


plt.bar([150,180,200],height=a,width=1.0,bottom=2.0)
plt.title('台積電收盤價分布柱状图')

plt.bar([150,180,200],height=a,width=15,bottom=2.0)
plt.title('台積電收盤價分布柱状图')


plt.bar(left=[150,180,200],height=a,width=15,bottom=2.0,color='red',edgecolor='k')
plt.title('台積電收盤價分布柱状图')

plt.barh([150,180,200],a,height=15,color='red',edgecolor='k')
plt.title('台積電收盤價分布柱状图')

plt.hist(Close,bins=12)
plt.title('台積電收盤價分布直方图')

plt.hist(Close,range=(120,200.20),orientation='horizontal',color='red',edgecolor='blue')
plt.title('台積電收盤價分布直方图')

plt.hist(Close,range=(120,200.20),orientation='vertical',cumulative=True,
         histtype='stepfilled',color='red',edgecolor='blue')
plt.title('台積電收盤價累積分布直方图')

plt.pie(a,labels=('（120,150]','(150,180]','(180,200]'),\
        colors=('b', 'g', 'r'),shadow=True) 
plt.title('台積電收盤價分布餅圖')

import numpy as np
prcData=TSMC.iloc[:,:4]
data=np.array(prcData)
plt.boxplot(data,labels=('Close','Open','High','Low'))
plt.title('台積電股價盒鬚圖')

fig=plt.figure()
plt.show()

ax1=fig.add_axes([0.1, 0.1, 0.3, 0.3])
ax2=fig.add_axes([0.5, 0.5, 0.4, 0.4])
ax1.plot(Close[:10])
ax2.plot(Open[:10])
plt.show()


ax1.set_title('前十個交易日收盤價')
ax1.set_xlabel('日期')
ax1.set_xticklabels(Close.index[:10],rotation=25)
ax1.set_ylabel('收盤價')
ax1.set_ylim(120,200)
ax2.set_title('前十個交易日開盤價')
ax2.set_xlabel('日期') 
ax2.set_xticklabels(Open.index[:10],rotation=25)
ax2.set_ylabel('開盤價')
ax2.set_ylim(120,200)

ax1=plt.subplot(221)
ax2=plt.subplot(222)
ax3=plt.subplot(223)
ax4=plt.subplot(224)


ax1=plt.subplot(211)
ax1.plot(Close,color='k')
ax1.set_ylabel('收盤價')
ax1.set_title('台積電2016年收盤價曲线图')

Volume=TSMC.Volume
ax2=plt.subplot(212)
left1=Volume.index[Close>=Open]
hight1=Volume[left1]
ax2.bar(left1,hight1,color='r')
left2=Volume.index[Close<Open]
hight2=Volume[left2]
ax2.bar(left2,hight2,color='g')

ax2.set_ylabel('成交量')
ax2.set_title('台積電2016年成交量柱狀圖')

#提取價格數據
High=TSMC.High
Low=TSMC.Low

fig=plt.figure()
ax=fig.add_axes([0.1,0.1,0.8,0.8])


ax.plot(Close[:'2016-03-01'],label='收盤價')
ax.plot(Open[:'2016-03-01'],'--*',label='開盤價')
ax.plot(High[:'2016-03-01'],'-+',label='最高價')
ax.plot(Low[:'2016-03-01'],'-.>',label='最低價')


ax.set_title('台積電2016年前2個月價格圖')
ax.set_ylabel('價格')
ax.legend(loc='best')


