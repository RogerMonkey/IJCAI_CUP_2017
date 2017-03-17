__author__ = 'Roger'

import pandas as pd
from statsmodels.tsa.stattools import adfuller

from prepare import *


## some test stationary for datas


# stationarity with ADF test
def test_stationarity(timeseries):
    # Determing rolling statistics
    # rolmean = pd.rolling_mean(timeseries, window=window)
    # rolstd = pd.rolling_std(timeseries, window=window)

    # Plot rolling statistics:
    #     orig = plt.plot(timeseries, color='blue',label='Original')
    #     mean = plt.plot(rolmean, color='red', label='Rolling Mean')
    #     std = plt.plot(rolstd, color='black', label = 'Rolling Std')
    #     plt.legend(loc='best')
    #     plt.title('Rolling Mean & Standard Deviation')
    #     plt.show(block=False)

    # Perform Dickey-Fuller test:
    # print('Results of Dickey-Fuller Test:')
    try:
        dftest = adfuller(timeseries, autolag='AIC')
        dfoutput = pd.Series(dftest[0:4],
                             index=['Test Statistic', 'p-value', '#Lags Used', 'Number of Observations Used'])
        for key, value in dftest[4].items():
            dfoutput['Critical Value (%s)' % key] = value
            #     print(dfoutput)
        if dfoutput['Test Statistic'] < dfoutput['Critical Value (1%)']:
            return dfoutput['p-value']
        else:
            return False
    except:
        return False


# count stationaryity
def count_stationaryity(timeseries, window):
    sum = 0
    for series in timeseries:
        if test_stationarity(timeseries[series], window) == True:
            sum += 1

    print(sum)


# test
if __name__ == '__main__':
    index, shop = load_data_as_npdict()
    sum = 0
    days = 61
    # time series
    pd_index = pd.date_range('2016-10-1', periods=days)
    for i in shop:
        # mean
        data = shop[i][-days:]
        data_mean = np.mean(data)
        for i in range(days):
            if data[i] < 0.01 * data_mean or data[i] > 3 * data_mean:
                data[i] = data_mean

        df = pd.Series(data, index=pd_index)
        value = test_stationarity(df, 7)
        # print(value['Test Statistic'])
        if value['Test Statistic'] < value['Critical Value (1%)']:
            sum += 1
            # print(data_mean)

    print(sum)
