'''
#Please use the following example commands to specify the path containing code and data:
import os
os.chdir('E:\\PythonBook_code_data\\part4')
'''

import pandas as pd
from statsmodels.tsa import stattools
from statsmodels.graphics.tsaplots import *
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
import numpy as np
from arch.unitroot import ADF

#讀取資料
taiex = pd.read_csv('taiex.csv',sep='\t')
taiex.index=pd.to_datetime(taiex.Date)

close=taiex.Close
taiexRet = (close-close.shift(1))/close
taiexRet.head()
taiexRet.tail()
taiexRet=taiexRet.dropna()

#計算自相關係數
acfs=stattools.acf(taiexRet)
acfs[:5]

#計算偏自相關係數
pacfs=stattools.pacf(taiexRet)
pacfs[:5]

#繪制自相關係數圖
from statsmodels.graphics.tsaplots import *
plot_acf(taiexRet,use_vlines=True,lags=30)


plot_pacf(taiexRet,use_vlines=True,lags=30)


close.plot()
plt.title('2014-2015年加權股價指數收盤指數時序圖 ')

taiexRet.plot()
plt.title('2014-2015年加權股價指數收益率指數時序圖')

plot_acf(taiexRet,use_vlines=True,lags=30)
plot_pacf(taiexRet,use_vlines=True,lags=30)
plot_acf(close,use_vlines=True,lags=30)

adf_taiexRet=ADF(taiexRet)
print(adf_taiexRet.summary().as_text())
adfclose=ADF(close)
print(adfclose.summary().as_text())


#生成純隨機序列
whiteNoise=np.random.standard_normal(size=500)

#繪制該序列圖
plt.plot(whiteNoise,c='b')
plt.title('White Noise')

LjungBox1=stattools.q_stat(stattools.acf(taiexRet)[1:13],len(taiexRet))
LjungBox1
LjungBox1[1][-1]

LjungBox2=stattools.q_stat(stattools.acf(close)[1:13],len(taiexRet))
LjungBox2[1][-1]

