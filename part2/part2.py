'''
#Please use the following example commands to specify the path containing code and data:
import os
os.chdir('E:\\PythonBook_code_data\\part2')
'''

# chap14
import pandas as pd
import matplotlib.pyplot as plt

returns=pd.read_csv('retdata.csv',sep='\t')
returns.head()
returns.tail()
returns.columns

HonHai=returns['Hon Hai Precision']
HonHai.describe()
plt.hist(HonHai)

TSMC = returns['TSMC         ']
UniPresident = returns['Uni-President']
TSMC.mean()
UniPresident.mean()

TSMC.median()
UniPresident.median()

TSMC.mode()
UniPresident.mode()

[TSMC.quantile(i) for i in [0.25,0.75]]
[UniPresident.quantile(i) for i in [0.25,0.75]]

TSMC.max()-TSMC.min()
TSMC.mad()
TSMC.var()
TSMC.std()
UniPresident.max()-UniPresident.min()
UniPresident.mad()
UniPresident.var()
UniPresident.std()



#chap15 
import numpy as np
import pandas as pd

RandomNumber=np.random.choice([1,2,3,4,5],\
                   size=100,replace=True,\
                   p=[0.1,0.1,0.3,0.3,0.2])
pd.Series(RandomNumber).value_counts()
pd.Series(RandomNumber).value_counts()/100

tw50=pd.read_csv('tw50.csv',sep='\t')
tw50.head(n=2)
tw50.ROI.describe()

import matplotlib.pyplot as plt
from scipy import stats
density=stats.kde.gaussian_kde(tw50.ROI)

bins=np.arange(-5,5,0.02) 

plt.subplot(211)
plt.plot(bins,density(bins))
plt.title('臺灣50指數收益率序列的概率密度曲線圖')

plt.subplot(212)
plt.plot(bins,density(bins).cumsum())
plt.title('臺灣50指數收益率序列的累積分布函數圖')

np.random.binomial(100,0.5,20)
np.random.binomial(10,0.5,3)

stats.binom.pmf(20,100,0.5)
stats.binom.pmf(50,100,0.5)

dd=stats.binom.pmf(np.arange(0,21,1),100,0.5)
dd
dd.sum()
stats.binom.cdf(20,100,0.5)

ret=tw50.ROI
ret.index = pd.to_datetime(tw50.Date)
ret1=ret['2016']
ret1.head(n=3)
len(ret1)
len(ret1[ret1>0])
p=len(ret1[ret1>0])/len(ret1)
p

prob=stats.binom.pmf(6,10,p)
prob

Norm=np.random.normal(size=5)
Norm

stats.norm.pdf(Norm)
stats.norm.cdf(Norm)

retMean=ret.mean()
retMean

retVariance=ret.var()
retVariance

stats.norm.ppf(0.05,retMean,
  retVariance**0.5)

plt.plot(np.arange(0,5,0.002),\
         stats.chi.pdf(np.arange(0,5,0.002),3))
plt.title('Probability Density Plot of Chi-Square Distribution')

x=np.arange(-4,4.004,0.004)
plt.plot(x,stats.norm.pdf(x),label='Normal')
plt.plot(x,stats.t.pdf(x,5),label='df=5')
plt.plot(x,stats.t.pdf(x,30),label='df=30')
plt.legend()

plt.plot(np.arange(0,5,0.002),\
        stats.f.pdf(np.arange(0,5,0.002),4,40))
plt.title('Probability Density Plot of F Distribution')


#correlation
TRD_Index=pd.read_table('index.csv',sep='\t')
TRD_Index.head()
np.unique(TRD_Index.CoName)
TRD_Index.index = pd.to_datetime(TRD_Index.Date)
Taiex=TRD_Index[TRD_Index.CoName=='TSE Taiex    ']
Taiex.head(3)

tw50=TRD_Index[TRD_Index.CoName=='TW 50 INDEX  ']
tw50.head(3)

retData = pd.concat([Taiex.ROI,tw50.ROI],axis=1).astype(np.float)
retData =retData.dropna()
retData.columns=['TAIEX','TW50']
retData.head()


plt.scatter(retData.TAIEX,retData.TW50)
plt.title('加權指數與50指數收益率的散點圖')
plt.xlabel('加權指數收益率')
plt.ylabel('50指數收益率') 

retData.TAIEX.corr(retData.TW50)


#chap16 
from scipy import stats
import numpy as np

x=[10.1 ,10 ,9.8 ,10.5 ,9.7,\
   10.1 ,9.9 ,10.2 ,10.3 ,9.9]

stats.t.interval(0.95,len(x)-1,\
              np.mean(x),stats.sem(x))

import pandas as pd
TRD_Index=pd.read_table('index.csv',sep='\t')
TRD_Index.index = pd.to_datetime(TRD_Index.Date)
Taiex=TRD_Index[TRD_Index.CoName=='TSE Taiex    ']
Taiex.head(3)
TaiexRet = Taiex.ROI.astype(np.float)
TaiexRet.hist()

mu=TaiexRet.mean()
sigma=TaiexRet.std()

import matplotlib.pyplot as plt
plt.hist(TaiexRet,normed=True)
plt.plot(np.arange(-4,4,0.002),\
   stats.norm.pdf(np.arange(-4,4,0.002),\
   mu,sigma))

stats.t.interval(0.95,len(TaiexRet)-1,mu,stats.sem(TaiexRet))


stats.ttest_1samp(TaiexRet,0)


tw50=TRD_Index[TRD_Index.CoName=='TW 50 INDEX  ']
tw50.head(3)

TM100=TRD_Index[TRD_Index.CoName=='TW MID-CAP INDEX']
TM100.head(3)



retData1 = pd.concat([TM100.ROI,tw50.ROI],axis=1).astype(np.float)
retData1 =retData1.dropna()
retData1.columns=['TM100','TW50']
stats.ttest_ind(retData1.TM100,retData1.TW50)


retData2 = pd.concat([Taiex.ROI,tw50.ROI],axis=1).astype(np.float)
retData2 =retData2.dropna()
retData2.columns=['Taiex','TW50']
stats.ttest_rel(retData2.Taiex,retData2.TW50)

#chap17
import pandas as pd
import statsmodels.stats.anova as anova
from statsmodels.formula.api import ols

year_return=pd.read_csv('TRD_Year.csv',\
                        encoding='gbk')
year_return.head()


model=ols('Return ~ C(Industry)',\
          data=year_return.dropna()).fit()
table1 = anova.anova_lm(model)
print(table1)

PSID=pd.read_csv('PSID.csv')
PSID.head(3)

model=ols('earnings ~C(married)+C(educatn)',\
           data=PSID.dropna()).fit()
table2 = anova.anova_lm(model)
print(table2)

model=ols('earnings ~ C(married)*C(educatn)', data=PSID.dropna()).fit()
table3 = anova.anova_lm(model)
print(table3)

#chap18
import pandas as pd
import numpy as np
TRD_Index=pd.read_table('index.csv',sep='\t')
TRD_Index.index = pd.to_datetime(TRD_Index.Date)
Taiex=TRD_Index[TRD_Index.CoName=='TSE Taiex    ']
tw50=TRD_Index[TRD_Index.CoName=='TW 50 INDEX  ']
retData = pd.concat([Taiex.ROI,tw50.ROI],axis=1).astype(np.float)
retData =retData.dropna()
retData.columns=['TAIEX','TW50']


import statsmodels.api as sm
model=sm.OLS(retData.TAIEX,sm.add_constant(retData.TW50)).fit()
print(model.summary())
model.fittedvalues[:5]

import matplotlib.pyplot as plt
plt.scatter(model.fittedvalues,model.resid)
plt.xlabel('擬合值')
plt.ylabel('殘差')

import scipy.stats as stats
sm.qqplot(model.resid_pearson,
              stats.norm,line='45')

plt.scatter(model.fittedvalues,\
             model.resid_pearson**0.5)
plt.xlabel('拟合值')
plt.ylabel('標准化殘差的平方根')

penn=pd.read_excel('Penn World Table.xlsx',2)
penn.head(3)

model=sm.OLS(np.log(penn.rgdpe),
             sm.add_constant(penn.iloc[:,-6:])).fit()

print(model.summary())

penn.iloc[:,-6:].corr()

model=sm.OLS(np.log(penn.rgdpe),\
             sm.add_constant(penn.iloc[:,-5:-1])).fit()

print(model.summary())