# -*- coding: utf-8 -*-
import pandas as pd
from pandas import DataFrame
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.ensemble import RandomForestRegressor
import numpy as np
import time
import sys
from unit import repeat_result
'''
'''
version = time.strftime('%Y-%m-%d', time.localtime(time.time())) + '_'

train_x = pd.read_csv('../../data/test_train/' + version + 'train_on_x.csv')
train_y = pd.read_csv('../../data/test_train/' + version + 'train_on_y.csv')
test_x = pd.read_csv('../../data/test_train/' + version + 'test_on_x.csv')

ET = RandomForestRegressor(n_estimators=2000, random_state=1, n_jobs=-1, min_samples_split=2, min_samples_leaf=2,
                         max_depth=25)

ET.fit(train_x, train_y)
pre = (ET.predict(test_x) + 0.5).round()
features = ET.feature_importances_
feature_sort = (features / np.sum(features) * 100).round(4)
feature_index = np.argsort(feature_sort)
for i in feature_index:
    print'{0} : {1}'.format(train_x.columns[i], feature_sort[i])
pre=repeat_result(pre)
np.savetxt('../../data/results/result_' + version + '.csv', np.concatenate((np.arange(1, 2001).reshape(2000, 1), pre), axis=1), delimiter=',',
               fmt='%d')
