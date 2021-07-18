
import UNI_v3_funcs as liq_amounts
import numpy as np
import pandas as pd

#Pool features
decimals0=6
decimals1=18
step=60 #fee_tier
test=pd.DataFrame()

#Ticks ETH/USDC pool
tick_lower=196740
tick_upper=201120
tick_entry=198740
sqrt_entry=(1.0001**(tick_entry/2)*(2**96))

test['ticks']=np.arange(tick_lower,tick_upper,step)
test['sqrt']=(1.0001**(test['ticks']/2)*(2**96))
test['sqrtA']=(1.0001**(tick_lower/2)*(2**96))
test['sqrtB']=(1.0001**(tick_upper/2)*(2**96))

relation_token= abs(liq_amounts.amounts_relation (tick_entry,tick_lower,tick_upper,decimals0,decimals1))
amount1=1
amount0=1/relation_token
initial_liquidity= liq_amounts.get_liquidity(sqrt_entry,test['sqrtA'].iloc[0],test['sqrtB'].iloc[0],amount0,amount1,decimals0,decimals1)   
test['liquidity']=initial_liquidity

test['amounts_0']=test.apply(lambda x: liq_amounts.get_amounts(x['sqrt'],x['sqrtA'],x['sqrtB'],x['liquidity'],decimals0,decimals1)[0] ,axis=1)
test['amounts_1']=test.apply(lambda x: liq_amounts.get_amounts(x['sqrt'],x['sqrtA'],x['sqrtB'],x['liquidity'],decimals0,decimals1)[1] ,axis=1)

test['price_t1/t0']=1/(1.0001**test['ticks']/10**(decimals1-decimals0))

test['value_LP']=test['amounts_1']*test['price_t1/t0']+test['amounts_0']
test['value_Hold']=amount1*test['price_t1/t0']+amount0
test['IL_USD']=test['value_LP']-test['value_Hold']
test['ILvsHold']=test['IL_USD']/test['value_Hold']


import matplotlib.pyplot as plt
plt.plot(test['price_t1/t0'],test['IL_USD'])
# plt.plot(test['price_t1/t0'],test['ILvsHold'])
plt.show()
print(1)







