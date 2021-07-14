
'''
Please use the following example commands to specify the path containing code and data:
import os
os.chdir('E:\\PythonBook_code_data\\part4\\027')
'''

import pandas as pd
import matplotlib.pyplot as plt
import math
from matplotlib.font_manager import FontProperties
#font=FontProperties(fname='C:/Windows/Fonts/msyh.ttf')

#導入ADF函數和numpy包
from arch.unitroot import ADF
import numpy as np
import re
import statsmodels.api as sm
from statsmodels.tsa.stattools import adfuller

KYE=pd.read_csv('2365.csv',sep='\t',index_col='Date')
KYE.index=pd.to_datetime(KYE.index)

Hitron=pd.read_csv('2419.csv',sep='\t',index_col='Date')
Hitron.index=pd.to_datetime(Hitron.index)


formStart='2014-01-01'
formEnd='2015-01-01'

KYEf=KYE[formStart:formEnd]
Hitronf=Hitron[formStart:formEnd]
KYEf.head()
Hitronf.head()
pairf=pd.concat([KYEf.Close,Hitronf.Close],axis = 1)
pairf.columns = ['昆盈','仲琦科技']
len(pairf)
pairf.plot(title='2014年收盤價圖')

def SSD(priceX,priceY):
    if priceX is None or priceY is None:
        print('缺少價格序列.')
    standardX=priceX/priceX[0]
    standardY=priceY/priceY[0]
    SSD=np.sum((standardX-standardY)**2)
    return(SSD) 

KYEf =  pairf['昆盈']  
Hitronf = pairf['仲琦科技'] 
dis=SSD(KYEf,Hitronf)
dis


KYEflog=np.log(KYEf)
adfA=ADF(KYEflog)
print(adfA.summary().as_text())

retA=KYEflog.diff()[1:]
adfretA=ADF(retA)
print(adfretA.summary().as_text())

Hitronflog=np.log(Hitronf)
adfB=ADF(Hitronflog)
print(adfB.summary().as_text())

retB=Hitronflog.diff()[1:]
adfretB=ADF(retB)
print(adfretB.summary().as_text())

KYEflog.plot(label='昆盈',style='--')
Hitronflog.plot(label='仲琦科技',style='r-')
plt.legend(loc='upper left')
plt.title('昆盈與仲琦科技的對數價格時序圖') 

retA.plot(label='昆盈',style='--')
retB.plot(label='仲琦科技',style='r-')
plt.legend(loc='lower left')
plt.title('昆盈與仲琦科技的對數價格差分(收益率)時序圖') 

#回歸分析 
#因變數是昆盈(A)股票的對數價格 
#自變數是仲琦科技(B)股票的對數價格

model=sm.OLS(KYEflog,sm.add_constant(Hitronflog))
results=model.fit()
print(results.summary())

alpha=results.params[0]  
beta=results.params[1]
spread=KYEflog-beta*Hitronflog-alpha
spread.head()

spread.plot()
plt.title('昆盈與仲琦科技的價差序列') 

adfSpread=ADF(spread, trend='nc') 
print(adfSpread.summary().as_text())

#最小距離法交易策略
standardA= KYEf/KYEf[0]

standardB= Hitronf/Hitronf[0]

SSD_pair=standardA-standardB

SSD_pair.head() 

meanSSD_pair=np.mean(SSD_pair)

sdSSD_pair=np.std(SSD_pair)

thresholdUp=meanSSD_pair+1.5*sdSSD_pair

thresholdDown=meanSSD_pair-1.5*sdSSD_pair


SSD_pair.plot()
plt.title('昆盈與仲琦科技標準化價差序列(形成期)') 
plt.axhline(y=meanSSD_pair,color='black')
plt.axhline(y=thresholdUp,color='red')
plt.axhline(y=thresholdDown,color='red') 
plt.show()

tradStart='2015-01-01'
tradEnd='2015-06-30'

KYEt=KYE[tradStart:tradEnd].Close
Hitront=Hitron[tradStart:tradEnd].Close

def spreadCal(priceX,priceY):
    data = pd.concat([priceX,priceY],axis=1).dropna()
    data.columns=['X','Y']
    standardX=data.X/data.X[0]
    standardY=data.Y/data.Y[0]
    spread=standardX-standardY
    return(spread)

TradSpread=spreadCal(KYEt,Hitront)
TradSpread.describe() 
 
TradSpread.plot()
plt.title('交易期價差序列')
plt.axhline(y=meanSSD_pair,color='black')
plt.axhline(y=thresholdUp,color='red')
plt.axhline(y=thresholdDown,color='red') 

spreadf=KYEflog-beta*Hitronflog-alpha
mu=np.mean(spreadf)
sd=np.std(spreadf)
mu+1.2*sd
mu-1.2*sd


CoSpreadT=np.log(KYEt)-beta*np.log(Hitront)-alpha
CoSpreadT.describe() 

CoSpreadT.plot()
plt.title('交易期價差序列(協整配對)')
plt.axhline(y=mu,color='black')
plt.axhline(y=mu+1.2*sd,color='red')
plt.axhline(y=mu-1.2*sd,color='red') 

######PairTrading Class #############

class PairTrading:
    def SSD(self,priceX,priceY):
        if priceX is None or priceY is None:
            print('缺少價格序列.')
        standardX=priceX/priceX[0]
        standardY=priceY/priceY[0]
        SSD=np.sum((standardY-standardX)**2)
        return(SSD)
    def SSDSpread(self,priceX,priceY):
        if priceX is None or priceY is None:
            print('缺少價格序列.')
        standardX=priceX/priceX[0]
        standardY=priceY/priceY[0]
        spread=standardY-standardX
        return(spread)
    def cointegration(self,priceX,priceY):
        if priceX is None or priceY is None:
            print('缺少價格序列.')
        priceX=np.log(priceX)
        priceY=np.log(priceY)
        results=sm.OLS(priceY,sm.add_constant(priceX)).fit()
        resid=results.resid
        adfSpread=ADF(resid)
        if adfSpread.pvalue>=0.05:
            print('''交易價格不具有協整關係.
            P-value of ADF test: %f
            Coefficients of regression:
            Intercept: %f
            Beta: %f
             ''' % (adfSpread.pvalue, results.params[0], results.params[1]))
            return(None)
        else:
            print('''交易價格具有協整關係.
            P-value of ADF test: %f
            Coefficients of regression:
            Intercept: %f
            Beta: %f
             ''' % (adfSpread.pvalue, results.params[0], results.params[1]))
            return(results.params[0], results.params[1])
    def CointegrationSpread(self,priceX,priceY,
                            formStart,formEnd,tradeStart,tradeEnd):
        if priceX is None or priceY is None:
            print('缺少價格序列.')
        formX=priceX[formStart:formEnd]
        formY=priceY[formStart:formEnd]
        tradeX=priceX[tradeStart:tradeEnd]
        tradeY=priceY[tradeStart:tradeEnd]
        coefficients=self.cointegration(formX,formY)
        if coefficients is None:
                print('未形成協整關係,無法配對.')
        else:
            spread=(np.log(tradeY)
            -coefficients[0]-coefficients[1]*np.log(tradeX))
            return(spread)
    def calBound(self,priceX,priceY,method,formStart,formEnd,width=1.5):
        formX=priceX[formStart:formEnd]
        formY=priceY[formStart:formEnd]
        if method=='SSD':
            spread=self.SSDSpread(formX,formY)            
            mu=np.mean(spread)
            sd=np.std(spread)
            UpperBound=mu+width*sd
            LowerBound=mu-width*sd
            return(UpperBound,LowerBound)
        elif method=='Cointegration':
            spread=self.CointegrationSpread(priceX,priceY,formStart,formEnd,
                 formStart,formEnd)
            mu=np.mean(spread)
            sd=np.std(spread)
            UpperBound=mu+width*sd
            LowerBound=mu-width*sd
            return(UpperBound,LowerBound)
        else:
            print('不存在該方法. 請選擇"SSD"或是"Cointegration".')




formStart = '2014-01-01'
formEnd = '2015-01-01'
tradeStart = '2015-01-01'
tradeEnd = '2015-06-30'


priceA= Hitron.Close
priceB=KYE.Close
priceAf=priceA[formStart:formEnd]
priceBf=priceB[formStart:formEnd]
priceAt=priceA[tradeStart:tradeEnd]
priceBt=priceB[tradeStart:tradeEnd]

pt=PairTrading()
SSD=pt.SSD(priceAf,priceBf)
SSD

SSDspread=pt.SSDSpread(priceAf,priceBf)
SSDspread.describe()
SSDspread.head()

coefficients=pt.cointegration(priceAf,priceBf)
coefficients
alpha
beta

CoSpreadF=pt.CointegrationSpread(priceA,priceB,
             formStart,formEnd,formStart,formEnd)
CoSpreadF.head()


CoSpreadTr=pt.CointegrationSpread(priceA,priceB,formStart,formEnd,
            tradeStart,tradeEnd)
CoSpreadTr.describe()

bound=pt.calBound(priceA,priceB,'Cointegration',
      formStart,formEnd,width=1.2)
bound

##########配對交易實測 ###############
mu=np.mean(CoSpreadF)
sd=np.std(CoSpreadF)


#設定交易期
CoSpreadTr.plot()
plt.title('交易期價差序列(協整配對)')
plt.axhline(y=mu,color='black')
plt.axhline(y=mu+0.2*sd,color='blue',ls='-',lw=2)
plt.axhline(y=mu-0.2*sd,color='blue',ls='-',lw=2)
plt.axhline(y=mu+1.5*sd,color='green',ls='--',lw=2.5)
plt.axhline(y=mu-1.5*sd,color='green',ls='--',lw=2.5)
plt.axhline(y=mu+2.5*sd,color='red',ls='-.',lw=3) 
plt.axhline(y=mu-2.5*sd,color='red',ls='-.',lw=3) 


level=(float('-inf'),mu-2.5*sd,
    mu-1.5*sd,mu-0.2*sd,
    mu+0.2*sd,mu+1.5*sd,
    mu+2.5*sd,
    float('inf'))

prcLevel=pd.cut(CoSpreadTr,level,labels=False)-3

prcLevel.head() 

def TradeSig(prcLevel):
    n=len(prcLevel)
    signal=np.zeros(n)
    for i in range(1,n):
        if prcLevel[i-1]==1 and prcLevel[i]==2:
            signal[i]=-2
        elif prcLevel[i-1]==1 and prcLevel[i]==0:
            signal[i]=2
        elif prcLevel[i-1]==2 and prcLevel[i]==3:
            signal[i]=3
        elif prcLevel[i-1]==-1 and prcLevel[i]==-2:
            signal[i]=1
        elif prcLevel[i-1]==-1 and prcLevel[i]==0:
            signal[i]=-1
        elif prcLevel[i-1]==-2 and prcLevel[i]==-3:
            signal[i]=-3
    return(signal)

signal=TradeSig(prcLevel)

position=[signal[0]]
ns=len(signal)

for i in range(1,ns):
    position.append(position[-1])
    if signal[i]==1:
        position[i]=1
    elif signal[i]==-2:
        position[i]=-1
    elif signal[i]==-1 and position[i-1]==1:
        position[i]=0
    elif signal[i]==2 and position[i-1]==-1:
        position[i]=0
    elif signal[i]==3:
        position[i]=0
    elif signal[i]==-3:
        position[i]=0

position=pd.Series(position,index=CoSpreadT.index)

position.tail() 

def TradeSim(priceX,priceY,position):
    n=len(position)
    shareY=10000*position
    shareX=[(-beta)*shareY[0]*priceY[0]/priceX[0]]
    cash=[10000]
    for i in range(1,n):
        shareX.append(shareX[i-1])
        cash.append(cash[i-1])
        if position[i-1]==0 and position[i]==1:
            shareX[i]=(-beta)*shareY[i]*priceY[i]/priceX[i]
            cash[i]=cash[i-1]-(shareY[i]*priceY[i]+shareX[i]*priceX[i])
        elif position[i-1]==0 and position[i]==-1:
            shareX[i]=(-beta)*shareY[i]*priceY[i]/priceX[i]
            cash[i]=cash[i-1]-(shareY[i]*priceY[i]+shareX[i]*priceX[i])
        elif position[i-1]==1 and position[i]==0:
            shareX[i]=0
            cash[i]=cash[i-1]+(shareY[i-1]*priceY[i]+shareX[i-1]*priceX[i])
        elif position[i-1]==-1 and position[i]==0:
            shareX[i]=0
            cash[i]=cash[i-1]+(shareY[i-1]*priceY[i]+shareX[i-1]*priceX[i])
    cash = pd.Series(cash,index=position.index)
    shareY=pd.Series(shareY,index=position.index)
    shareX=pd.Series(shareX,index=position.index)
    asset=cash+shareY*priceY+shareX*priceX
    account=pd.DataFrame({'Position':position,'ShareY':shareY,'ShareX':shareX,'Cash':cash,'Asset':asset})
    return(account)


account1=TradeSim(Hitront,KYEt,position)
account1.tail() 
account1.ix[-1,'Asset']

plt.subplot(211)
plt.plot(account1.Asset,label='asset')
plt.title('配對交易賬戶') 
plt.legend()
plt.ylabel('asset')
plt.subplot(212)
plt.plot(account1.ShareX,label='仲琦科技')
plt.plot(account1.ShareY,':',label='昆盈')
plt.ylabel('share')
plt.title('配對交易倉位情況')
plt.legend()
plt.show()

