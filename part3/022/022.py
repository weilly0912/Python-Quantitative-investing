'''
#Please use the following example commands to specify the path containing code and data:
import os
os.chdir('E:\\PythonBook_code_data\\part3\\022')
'''

import pandas as pd
stock=pd.read_csv('retdata.csv',sep='\t')
stock.head(n=3)
stock.index = pd.to_datetime(stock.Date)
UniPresident = stock.iloc[:,3]
UniPresident.head(n=3)


factors=pd.read_csv('factors.csv',sep='\t')
factors.head(n=3)
factors.index =pd.to_datetime(factors['YY/MM/DD']) 
factors.columns

factors['Risk-free Interest Rate']=(factors['Risk-free Interest Rate']**(1/360)-1)*100
factors.head(n=3)


data=pd.concat([UniPresident,factors.iloc[:,1:]],axis=1).dropna()
data.tail(n=3)

data['Uni-President'] = data['Uni-President'] - data['Risk-free Interest Rate']


import statsmodels.api as sm
regThrFac=sm.OLS(data['Uni-President'],sm.add_constant(data.iloc[:,1:4]))
result=regThrFac.fit()
result.summary()

result.params