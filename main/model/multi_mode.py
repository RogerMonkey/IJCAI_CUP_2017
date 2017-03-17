# -*- coding: utf-8 -*-

import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.ensemble import ExtraTreesRegressor
import sys
import numpy as np
import random
import time
from unit import *
feature_more_or_less = "_less_feature"  # _more_feature
version = time.strftime('%Y-%m-%d', time.localtime(time.time())) + '_'

train_x = pd.read_csv('../../data/test_train/' + version + feature_more_or_less + 'train_off_x.csv')
train_y = pd.read_csv('../../data/test_train/' + version  + feature_more_or_less+ 'train_off_y.csv')
test_x = pd.read_csv('../../data/test_train/' + version + feature_more_or_less + 'test_off_x.csv')
test_y = pd.read_csv('../../data/test_train/' + version + feature_more_or_less + 'test_off_y.csv')

clfs = [ExtraTreesRegressor(n_estimators=1200, random_state=1, n_jobs=-1, min_samples_split=2, min_samples_leaf=2,
                            max_depth=25, max_features=45),
        ExtraTreesRegressor(n_estimators=1200, random_state=1, n_jobs=-1, min_samples_split=2, min_samples_leaf=2,
                            max_depth=25, max_features=30),
        ExtraTreesRegressor(n_estimators=1200, random_state=1, n_jobs=-1, min_samples_split=2, min_samples_leaf=2,
                            max_depth=25, max_features=20)
        ]

train_x_pre = []  # train_x.values.tolist()
test_x_pre = []  # test_x.values.tolist()
ans=np.zeros((2000,7))
for clf in clfs:
    clf.fit(train_x, train_y)
    train_pre = (clf.predict(train_x) + 0.5).round()
    test_pre = (clf.predict(test_x) + 0.5).round()
    score = calcscore(test_pre, test_y.values)
    print score
    ans+=test_pre


feature_more_or_less = "_more_feature"

train_x = pd.read_csv('../../data/test_train/' + version + feature_more_or_less + 'train_off_x.csv')
train_y = pd.read_csv('../../data/test_train/' + version  + feature_more_or_less+ 'train_off_y.csv')
test_x = pd.read_csv('../../data/test_train/' + version + feature_more_or_less + 'test_off_x.csv')
test_y = pd.read_csv('../../data/test_train/' + version + feature_more_or_less + 'test_off_y.csv')
#
print train_x.shape[1]

clfs = [ExtraTreesRegressor(n_estimators=1200, random_state=1, n_jobs=-1, min_samples_split=2, min_samples_leaf=2,
                            max_depth=25, max_features=190),
        ExtraTreesRegressor(n_estimators=1200, random_state=1, n_jobs=-1, min_samples_split=2, min_samples_leaf=2,
                            max_depth=25, max_features=160),
        ExtraTreesRegressor(n_estimators=1200, random_state=1, n_jobs=-1, min_samples_split=2, min_samples_leaf=2,
                            max_depth=25, max_features=130),
        ]

print ">>>>>>>>>>>>>>>>>>>>>>>>>>>"
score = calcscore(ans/3, test_y.values)
print score

for clf in clfs:
    clf.fit(train_x, train_y)
    train_pre = (clf.predict(train_x) + 0.5).round()
    test_pre = (clf.predict(test_x) + 0.5).round()
    score = calcscore(test_pre, test_y.values)
    print score
    ans += test_pre

ans=ans/6
score = calcscore(ans, test_y.values)
print score
