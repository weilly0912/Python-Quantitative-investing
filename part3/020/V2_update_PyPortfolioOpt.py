'''
Please use the following example commands to specify the path containing code and data:
import os
os.chdir('E:\\book_data\\part 3\\019')
'''

import numpy as np
import math
import matplotlib.pyplot as plt
def cal_mean(frac):
    return(0.08*frac+0.15*(1-frac))

mean=list(map(cal_mean,[x/50 for x in range(51)]))
sd_mat=np.array([list(map(lambda x: math.sqrt((x**2)*0.12**2+
((1-x)**2)*0.25**2+2*x*(1-x)*(-1.5+i*0.5)*0.12*0.25),[x/50 for x in range(51)])
) for i in range(1,6)])
#[expression for variable in sequence] list comprehension
plt.plot(sd_mat[0,:],mean,label='-1')
plt.plot(sd_mat[1,:],mean,label='-0.5')
plt.plot(sd_mat[2,:],mean,label='0')
plt.plot(sd_mat[3,:],mean,label='0.5')
plt.plot(sd_mat[4,:],mean,label='1')
plt.legend(loc='upper left')

import pandas as pd
retData = pd.read_csv('retdata.csv',
                      sep='\t',index_col='Date')
retData.index = pd.to_datetime(retData.index)
retData = retData*0.01
retData.head()



cumreturn=(1+retData).cumprod()-1
cumreturn.plot()
plt.title('Cumulative Return of 3 Stocks(2014-2016)')
plt.legend(loc='lower center',bbox_to_anchor=(0.5,-0.3),
          ncol=5, fancybox=True, shadow=True)
          
retData=retData.dropna()
retData.corr()

import numpy as np
import pandas as pd
#import portfolioopt as pfopt
from pypfopt import EfficientFrontier
'''
The portfolioopt package has not been updated for 5 years.
We replace the portfolioopt package with the PyPortfolioOpt package.
https://github.com/robertmartin8/PyPortfolioOpt
https://pyportfolioopt.readthedocs.io/en/latest/EfficientFrontier.html
'''

train_set=retData['2014-01-01':'2015-12-31']
test_set=retData['2016']

cov_mat =train_set.cov()
avg_rets = train_set.mean()

#only long 
target_ret = 0.0006


#weights = pfopt.markowitz_portfolio(cov_mat, avg_rets, target_ret,
#  allow_short=False)
#weights


ef = EfficientFrontier(avg_rets, cov_mat)
weights=ef.efficient_return(target_return=target_ret)
weights

weights=pd.DataFrame(weights.values(),index=weights.keys())                     

test_return=np.dot(test_set,
                   weights)
test_return=pd.DataFrame(test_return,index=test_set.index)
test_cum_return=(1+test_return).cumprod()-1
test_cum_return.columns = ['markowitz_portfolio']
test_cum_return.head()

sim_weight=np.random.uniform(0,1,(100,3))
sim_weight_normalized =np.apply_along_axis(lambda x: x/sum(x),1,sim_weight)

sim_return=np.dot(test_set,np.matrix(sim_weight_normalized).T)
sim_return=pd.DataFrame(sim_return,index=test_set.index)
sim_cum_return=(1+sim_return).cumprod()-1


plt.plot(sim_cum_return.index,sim_cum_return,color='green')
plt.plot(test_cum_return.index,test_cum_return,color='red')
plt.title('資產組合累積收益率（Markowitz模型與 隨機配比）')

from scipy import linalg

def blacklitterman(returns,tau, P, Q):
  mu=returns.mean()
  sigma=returns.cov()
  pi1=mu
  ts = tau * sigma
  Omega = np.dot(np.dot(P,ts),P.T) * np.eye(Q.shape[0])
  middle = linalg.inv(np.dot(np.dot(P,ts),P.T) + Omega)  
  er = np.expand_dims(pi1,axis=0).T + np.dot(np.dot(np.dot(ts,P.T),middle),
                      (Q - np.expand_dims(np.dot(P,pi1.T),axis=1)))
  posteriorSigma = sigma + ts - np.dot(ts.dot(P.T).dot(middle).dot(P),ts)
  return [er, posteriorSigma]
  
pick1=np.array([1,1,0])
q1=np.array([0.0009])
pick2=np.array([1,0,-1])
q2=np.array([0.0003])
P=np.array([pick1,pick2])
Q=np.array([q1,q2])
P
Q

res=blacklitterman(retData,0.1, P, Q)
p_mean=pd.DataFrame(res[0],index=retData.columns,columns=['posterior_mean'])
p_mean
p_cov=res[1]
p_cov


target_ret2 = 0.0006
cov_mat2 = res[1]
avg_rets2 = pd.Series(res[0][:,0],index=retData.columns)

#weights2 = pfopt.markowitz_portfolio(cov_mat2, avg_rets2, target_ret2,
#  allow_short=False)
#weights2


ef = EfficientFrontier(avg_rets2, cov_mat2)
weights2=ef.efficient_return(target_return=target_ret2)
weights2