import pandas as pd
import numpy as np

def smaCal(tsPrice,k):
    sma=pd.Series([np.nan]*len(tsPrice),index=tsPrice.index)
    for i in range(k-1,len(tsPrice)):
        sma[i]=np.mean(tsPrice[(i-k+1):(i+1)])
    return(sma)

def smaCal_gene(price,k):
    #priceList只存需要計算的k期股價數據
    #用first in first out的方式來存刪數據，進而體現移動的思想
    priceList=[]
    n = len(price)
    for i in range(n):
        #在priceList中增加最新一筆數據
        priceList.append(price[i])
        if len(priceList)==k:
            yield np.mean(priceList)
            #刪除priceList中第0期數據
            priceList.pop(0)

def wmaCal(tsPrice,weight):
    k=len(weight)
    arrWeight=np.array(weight)
    Wma=pd.Series([np.nan]*len(tsPrice),index=tsPrice.index)
    for i in range(k-1,len(tsPrice.index)):
        Wma[i]=sum(arrWeight*tsPrice[(i-k+1):(i+1)])
    return(Wma)

def wmaCal_gene(price,w):
    #priceList只存需要計算的k期股價數據
    #用first in first out的方式來存刪數據，進而體現移動的思想
    priceList=[]
    n = len(price)
    w=np.array(w)
    k=len(w)
    for i in range(n):
        #在priceList中增加最新一筆數據
        priceList.append(price[i])
        if len(priceList)==k:
            yield np.sum(np.array(priceList)*w)
            #刪除priceList中第0期數據
            priceList.pop(0)


def ewmaCal(tsprice,period=5,exponential=0.2):
   Ewma=pd.Series([np.nan]*len(tsprice),index=tsprice.index)
   Ewma[period-1]=np.mean(tsprice[:period])
   for i in range(period,len(tsprice)):
       Ewma[i]=exponential*tsprice[i]+(1-exponential)*Ewma[i-1]
   return(Ewma)

def ewmaCal_gene(price,k,e):
    for i in range(k-1,len(price)):
        if i==k-1:
            ewmaValue=np.mean(price[:k])
        else:
            ewmaValue=e*price[i]+(1-e)*ewmaValue
        yield ewmaValue
