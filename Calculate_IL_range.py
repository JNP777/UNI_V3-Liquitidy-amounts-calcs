import numpy as np
import pandas as pd
from UNI_v3_funcs import *
import matplotlib.pyplot as plt


class Pool_simualtion:
    def __init__(self, tick_upper, tick_lower, tick_entry):
        self.tick_upper = tick_upper
        self.tick_lower = tick_lower
        self.tick_entry = tick_entry
        self.decimals0 = 6
        self.decimals1 = 18
        self.tick_space = 80
        self.sqrt_entry = (1.0001 ** (self.tick_entry / 2) * (2 ** 96))
        self.df = pd.DataFrame()

        # Create vector with every tick_space in the range

    def create_df(self):
        self.df['ticks'] = np.arange(self.tick_lower, self.tick_upper, self.tick_space)
        self.df['sqrt'] = (1.0001 ** (self.df['ticks'] / 2) * (2 ** 96))
        self.df['sqrtA'] = (1.0001 ** (self.tick_lower / 2) * (2 ** 96))
        self.df['sqrtB'] = (1.0001 ** (self.tick_upper / 2) * (2 ** 96))

        # Calls liquidity amount formula to calculate the relation of tokens required to pool at time0
        relation_token = abs(
            amounts_relation(self.tick_entry, self.tick_lower, self.tick_upper, self.decimals0, self.decimals1))
        # Calculating amounts of token0 based on 1 unit of t1
        amount1 = 1
        amount0 = 1 / relation_token
        # Calls amountsforliquidity formula to get liquidity deployed
        initial_liquidity = get_liquidity(self.tick_entry, self.tick_lower,
                                          self.tick_upper, amount0,
                                          amount1, self.decimals0,
                                          self.decimals1)
        self.df['liquidity'] = initial_liquidity
        # Calculate amounts at every tick space based on liquidity for amounts0
        self.df['amounts_0'] = self.df.apply(lambda x: get_amounts(x['ticks'],
                                                                   self.tick_lower, self.tick_upper,
                                                                   x['liquidity'], self.decimals0,
                                                                   self.decimals1)[0], axis=1)
        # Calculate amounts at every tick space based on liquidity for amounts1
        self.df['amounts_1'] = self.df.apply(lambda x: get_amounts(x['ticks'],
                                                                   self.tick_lower, self.tick_upper,
                                                                   x['liquidity'], self.decimals0,
                                                                   self.decimals1)[1], axis=1)
        # Calculating price at every tick_space
        self.df['price_t1/t0'] = 1 / (1.0001 ** self.df['ticks'] / 10 ** (self.decimals1 - self.decimals0))

        # Calculating the value of the position in every tick_space
        self.df['value_LP'] = self.df['amounts_1'] * self.df['price_t1/t0'] + self.df['amounts_0']

        # Calculating the value of holding the initial amount of tokens
        self.df['value_Hold'] = amount1 * self.df['price_t1/t0'] + amount0

        # Calculating IL
        self.df['IL_USD'] = self.df['value_LP'] - self.df['value_Hold']
        self.df['ILvsHold'] = self.df['IL_USD'] / self.df['value_Hold']
        return self.df


# Ticks of the range to simulate
tick_lower = 197740
tick_upper = 198740
tick_entry = 199740

if __name__ == "__main__":
    df = Pool_simualtion(tick_upper, tick_lower, tick_entry).create_df()
    plt.plot(df['price_t1/t0'], df['IL_USD'])
    plt.show()
