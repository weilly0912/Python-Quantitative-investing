'''
#Please use the following example commands to specify the path containing code and data:
import os
os.chdir('E:\\PythonBook_code_data\\part3\\021')
'''

import pandas as pd
import numpy as np 
indexData=pd.read_csv('index.csv',sep='\t')
np.unique(indexData.CoName)
mktData=indexData[indexData.CoName=='TSE Taiex    ']
mktData.head()

mktret=pd.Series(mktData.ROI.values,index=pd.to_datetime(mktData.Date))
mktret.name='mktret'
mktret.head()



HeySong=pd.read_csv('1234.csv',sep='\t')
HeySong.index=pd.to_datetime(HeySong.Date)
HeySong.head()
HeySongret=HeySong.ROI
HeySongret.name='returns'

retData=pd.concat([HeySongret,mktret],axis=1).dropna() 
retData = retData.astype(np.float)*0.01
retData.head()
rf=1.0038**(1/360)-1
rf
Excess_ret=retData['2016']-rf
Excess_ret.tail()

import matplotlib.pyplot as plt
plt.scatter(Excess_ret.values[:,0],Excess_ret.values[:,1])
plt.title('HeySong return and market return')

import statsmodels.api as sm
model=sm.OLS(Excess_ret.returns[1:],sm.add_constant(Excess_ret.mktret[1:]))
result=model.fit()
result.summary()