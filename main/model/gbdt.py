# -*- coding: utf-8 -*-
import pandas as pd
from pandas import DataFrame
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.ensemble import RandomForestRegressor
import numpy as np
import time
from unit import repeat_result
import sys

def gbdt():
    version = time.strftime('%Y-%m-%d', time.localtime(time.time())) + '_'

    train_x = pd.read_csv('../../data/test_train/' + version + 'train_on_x.csv')
    train_y = pd.read_csv('../../data/test_train/' + version + 'train_on_y.csv')
    test_x = pd.read_csv('../../data/test_train/' + version + 'test_on_x.csv')

    param = {'subsample': [1, 1, 1, 1, 1, 1, 1],
             'min_samples_leaf': [1, 1, 1, 1, 1, 1, 1],
             'n_estimators': [200, 100, 200, 200, 200, 200, 100],
             'min_samples_split': [4, 8, 2, 8, 2, 4, 4],
             'learning_rate': [0.05, 0.1, 0.05, 0.05, 0.05, 0.05, 0.1],
             'max_features': [270, 'auto', 280, 'auto', 270, 280, 270],
             'random_state': [1, 1, 1, 1, 1, 1, 1] ,
             'max_depth': [4, 6, 4, 4, 4, 4, 4]}

    result = DataFrame()

    for i in range(0, 7):
        GB = GradientBoostingRegressor(n_estimators=param['n_estimators'][i], learning_rate=0.05, random_state=1, \
                                       min_samples_split=param['min_samples_split'][i], min_samples_leaf=1,
                                       max_depth=param['max_depth'][i], max_features=param['max_features'][i],
                                       subsample=0.85)

        GB.fit(train_x, train_y.icol(i))
        pre = (GB.predict(test_x)).round()

        result['col' + str(i)] = pre
    pre=repeat_result(result.values)
    np.savetxt('../../data/results/result_' + version + '.csv', np.concatenate((np.arange(1, 2001).reshape(2000, 1), pre), axis=1), delimiter=',',
                   fmt='%d')

if __name__ == '__main__':
    run()