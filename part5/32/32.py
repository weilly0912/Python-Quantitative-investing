'''
Please use the following example commands to specify the path containing code and data:
import os
os.chdir('E:\\PythonBook_code_data\\part5\\32')

'''
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

HeySong = pd.read_csv('1234.csv',sep='\t')
HeySong.index=pd.to_datetime(HeySong.Date, format='%Y-%m-%d')

Close = HeySong.Close
High = HeySong.High
Low = HeySong.Low

upboundDC = [max(High[(i-20):i]) for i in range(20,len(Close))]

downboundDC = [min(Low[(i-20):i]) for i in range(20,len(Close))]

boundDC = pd.DataFrame()
boundDC['upboundDC']=upboundDC
boundDC['downboundDC']=downboundDC
boundDC['midboundDC']=0.5*(boundDC['upboundDC']+boundDC['downboundDC'])
boundDC.index = Close.index[20:]


plt.plot(Close[:'2015-06-30'],label="Close",color='k')
plt.plot(boundDC.upboundDC[:'2015-06-30'],
         label="upboundDC",color='b',
         linestyle='dashed')
plt.plot(boundDC.midboundDC[:'2015-06-30'],
         label="midboundDC",color='r',linestyle='-.')
plt.plot(boundDC.downboundDC[:'2015-06-30'],
         label="downboundDC",color='b',
         linestyle='dashed')
plt.title("2015年上半年黑松股價唐奇安通道")
plt.legend()


import candle
candle.candleLinePlots(candleData=HeySong[:'2015-06-30'],
        candleTitle='2015年上半年黑松股票的K線圖及唐奇安通道',
        splitFigures=False,
        Data=boundDC[:'2015-06-30'][['upboundDC','downboundDC']])


def upbreak(tsLine,tsRefLine):
    n=min(len(tsLine),len(tsRefLine))
    tsLine=tsLine[-n:]
    tsRefLine=tsRefLine[-n:]
    signal=pd.Series(0,index=tsLine.index)
    for i in range(1,len(tsLine)):
        if all([tsLine[i]>tsRefLine[i],tsLine[i-1]<tsRefLine[i-1]]):
            signal[i]=1
    return(signal)

def downbreak(tsLine,tsRefLine):
    n=min(len(tsLine),len(tsRefLine))
    tsLine=tsLine[-n:]
    tsRefLine=tsRefLine[-n:]
    signal=pd.Series(0,index=tsLine.index)
    for i in range(1,len(tsLine)):
        if all([tsLine[i]<tsRefLine[i],tsLine[i-1]>tsRefLine[i-1]]):
            signal[i]=1
    return(signal)

#DC Strategy
UpBreak=upbreak(Close[boundDC.index[0]:],boundDC.upboundDC)
DownBreak=downbreak(Close[boundDC.index[0]:],\
          boundDC.downboundDC)
BreakSig=UpBreak-DownBreak

tradeSig=BreakSig.shift(1)
ret=Close/Close.shift(1)-1
tradeRet=(ret*tradeSig).dropna()
tradeRet[tradeRet==-0]=0
winRate=len(tradeRet[tradeRet>0]\
            )/len(tradeRet[tradeRet!=0])
winRate


#BBands
def bbands(tsPrice,period=20,times=2):
    upBBand=pd.Series(0.0,index=tsPrice.index)
    midBBand=pd.Series(0.0,index=tsPrice.index)
    downBBand=pd.Series(0.0,index=tsPrice.index)
    sigma=pd.Series(0.0,index=tsPrice.index)
    for i in range(period-1,len(tsPrice)):
        midBBand[i]=np.nanmean(tsPrice[i-(period-1):(i+1)])
        sigma[i]=np.nanstd(tsPrice[i-(period-1):(i+1)])
        upBBand[i]=midBBand[i]+times*sigma[i]
        downBBand[i]=midBBand[i]-times*sigma[i]
    BBands=pd.DataFrame({'upBBand':upBBand[(period-1):],\
                         'midBBand':midBBand[(period-1):],\
                         'downBBand':downBBand[(period-1):],\
                         'sigma':sigma[(period-1):]})
    return(BBands)

HeySongBBands=bbands(Close,20,2)
HeySongBBands.head()


import candle
candle.candleLinePlots(candleData=HeySong[:'2015-06-30'],
        candleTitle='2015年上半年黑松股票的K線圖及布林帶通道',
        splitFigures=False,
        Data=HeySongBBands[:'2015-06-30'][['downBBand','upBBand']])




def CalBollRisk(tsPrice,k,multiplier):
    n=len(tsPrice)
    m=len(multiplier)
    tsPrice=tsPrice[k:]
    BollRisk=[]
    for i in range(m):
        BBands=bbands(tsPrice,k,multiplier[i])
        a=0
        b=0
        for j in range(len(BBands)):            
            if tsPrice[j]>BBands.upBBand[j]:
                a+=1
            elif tsPrice[j]<BBands.downBBand[j]:
                b+=1
        BollRisk.append(100*(a+b)/n)
    return(BollRisk)

multiplier=[1,1.65,1.96,2,2.58]
price2015=Close['2015']
CalBollRisk(price2015,20,multiplier)

CalBollRisk(Close['2016'],20,multiplier)


#strategy 1
BBands=bbands(Close,20,2)

upbreakBB1=upbreak(Close,BBands.upBBand)
downbreakBB1=downbreak(Close,BBands.downBBand)

upBBSig1=-upbreakBB1.shift(2)
downBBSig1=downbreakBB1.shift(2)

tradSignal1=upBBSig1+downBBSig1
tradSignal1[tradSignal1==-0]=0

def perform(tsPrice,tsTradSig):
    ret=tsPrice/tsPrice.shift(1)-1
    tradRet=(ret*tsTradSig).dropna()
    ret=ret[-len(tradRet):]
    winRate=[len(ret[ret>0])/len(ret[ret!=0]),\
             len(tradRet[tradRet>0])/len(tradRet[tradRet!=0])]
    meanWin=[np.mean(ret[ret>0]),\
             np.mean(tradRet[tradRet>0])]
    meanLoss=[np.mean(ret[ret<0]),\
             np.mean(tradRet[tradRet<0])]
    Performance=pd.DataFrame({'winRate':winRate,'meanWin':meanWin,\
                             'meanLoss':meanLoss})
    Performance.index=['Stock','Trade']
    return(Performance)

Performance1= perform(Close,tradSignal1)
Performance1

# strategy 2
upbreakBB2=upbreak(Close,BBands.downBBand)
downbreakBB2=downbreak(Close,BBands.upBBand)

upBBSig2=upbreakBB2.shift(2)
downBBSig2=-downbreakBB2.shift(2)
tradSignal2=upBBSig2+downBBSig2
tradSignal2[tradSignal2==-0]=0

Performance2= perform(Close,tradSignal2)
Performance2
