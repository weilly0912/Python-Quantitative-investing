'''
#Please use the following example commands to specify the path containing code and data:
import os
os.chdir('E:\\PythonBook_code_data\\part4')
'''

import pandas as pd
taiex=pd.read_csv('taiex.csv',sep='\t')

#檢視前3期數據
taiex.head(n=3)

#檢視數據taiex的類型
type(taiex)

#提取加權股價指數的收盤指數數據
Close=taiex.Close
Close.head(n=3)
type(Close)
type(Close.index)

#將收盤指數轉換成時間序列格式
Close.index=pd.to_datetime(taiex.Date)
Close.head()

#檢視Close的類型
type(Close)
#Close的index是日期數據

type(Close.index)

#最後，繪製時間序列圖
Close.plot()

#截取2015年10月8日到10月31日的數據
taiex.index = pd.to_datetime(taiex.Date)
taiex=taiex.iloc[:,1:]
taiexPart = taiex['2015-10-08':'2015-10-31']

#檢視前兩期數據
taiexPart.head(n=2)

#檢視後兩個交易數據
taiexPart.tail(n=2)

#截取2015年數據
taiex2015=taiex['2015']
#檢視2015年前2期交易數據
taiex2015.head(n=2)
#檢視後2期交易數據
taiex2015.tail(n=2)

#選取2015年初以後的數據
taiexAfter2015=taiex['2015':]
taiexAfter2015.head(n=2)
#選取2015年以前的數據
taiexBefore2015=taiex[:'2015-01-01']
taiexBefore2015.tail(n=2)

#選取2014年9月到年底的數據
taiex9End=taiex['2014-09':'2014']
taiex9End.head(n=2)
taiex9End.tail(n=2)

Close.head()
Close.tail(n=1)
Close.hist()
#求最大值
Close.max()
#求最小值
Close.min()
#求均值
Close.mean()
#求中位數
Close.median()
#求標準差
Close.std()
#總結數據分佈情況
Close.describe()
