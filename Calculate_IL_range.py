
import UNI_v3_funcs as liq_amounts
import numpy as np
import pandas as pd

#Pool features
decimals0=6
decimals1=18
tick_space=60 #fee_tier
test=pd.DataFrame()

#Ticks of the range to simulate
tick_lower=196740
tick_upper=201120
#Tick of the pool at time0
tick_entry=198740
sqrt_entry=(1.0001**(tick_entry/2)*(2**96))

#Create vector with every tick_space in the range


test['sqrt']=(1.0001**(test['ticks']/2)*(2**96))
test['sqrtA']=(1.0001**(tick_lower/2)*(2**96))
test['sqrtB']=(1.0001**(tick_upper/2)*(2**96))

#Calls liquidity amount formula to calculate the relation of tokens required to pool at time0
relation_token= abs(liq_amounts.amounts_relation (tick_entry,tick_lower,tick_upper,decimals0,decimals1))

#Calculating amounts of token0 based on 1 unit of t1
amount1=1
amount0=1/relation_token

#Calls amountsforliquidity formula to get liquidity deployed 
initial_liquidity= liq_amounts.get_liquidity(tick_entry,tick_lower,tick_upper,amount0,amount1,decimals0,decimals1)   
test['liquidity']=initial_liquidity
#Calculate amounts at every tick space based on liquidity
test['amounts_0']=test.apply(lambda x: liq_amounts.get_amounts(x['ticks'],tick_lower,tick_upper,x['liquidity'],decimals0,decimals1)[0] ,axis=1)
test['amounts_1']=test.apply(lambda x: liq_amounts.get_amounts(x['ticks'],tick_lower,tick_upper,x['liquidity'],decimals0,decimals1)[1] ,axis=1)

#Calculating price at every tick_space
test['price_t1/t0']=1/(1.0001**test['ticks']/10**(decimals1-decimals0))

#Calculating the value of the position in every tick_space
test['value_LP']=test['amounts_1']*test['price_t1/t0']+test['amounts_0']

#Calculating the value of holding the initial amount of tokens
test['value_Hold']=amount1*test['price_t1/t0']+amount0

#Calculating IL
test['IL_USD']=test['value_LP']-test['value_Hold']
test['ILvsHold']=test['IL_USD']/test['value_Hold']

#Plotting price vs IL
import matplotlib.pyplot as plt
plt.plot(test['price_t1/t0'],test['IL_USD'])
# plt.plot(test['price_t1/t0'],test['ILvsHold'])
plt.show()







