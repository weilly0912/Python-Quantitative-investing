'''
#Please use the following example commands to specify the path containing code and data:
import os
os.chdir('E:\\PythonBook_code_data\\part4\\026')
'''

import pandas as pd
from statsmodels.graphics.tsaplots import *
from statsmodels.tsa import stattools
import matplotlib.pyplot as plt

import numpy as np
from arch import arch_model

indexRet = pd.read_csv('index.csv',sep='\t')
indexRet.index=pd.to_datetime(indexRet.Date)
indexRet.head()
np.unique(indexRet.CoName)

taiexRet = indexRet.loc[indexRet.CoName=='TSE Taiex    '].ROI
taiexRet.head()
taiexRet.tail()
taiexRet = taiexRet.astype(np.float).dropna()
#繪制收益率平方序列圖
plt.subplot(211)
plt.plot(taiexRet**2)
plt.xticks([])
plt.title('Squared Daily Return of taiex')

plt.subplot(212)
plt.plot(np.abs(taiexRet))
plt.title('Absolute Daily Return of taiex')

LjungBox=stattools.q_stat(stattools.acf(taiexRet**2)[1:13],len(taiexRet))
LjungBox[1][-1]

am = arch_model(taiexRet)
model = am.fit(update_freq=0)
print(model.summary())