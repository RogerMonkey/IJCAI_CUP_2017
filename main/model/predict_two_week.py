# -*- coding: utf-8 -*-
import sys
from functools import reduce
from sklearn.ensemble import ExtraTreesRegressor, GradientBoostingRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.feature_selection import SelectFromModel
import time
from unit import *


'''
我们竞赛中主要使用的模型，使用sklearn的ExtraTreeRegress

1. 使用平滑所有的数据集
2. 线下offlineTest
    train ZA->BC
    test  AB->CD
3.线上onlineTest
    train ZAB->CD
    test  BCD->EF(ans)
4.使用ExtraTreesRegressor 连续预测14天数值

'''

#ET参数
params = {
    'n_estimators': 1662,
    'n_jobs': -1,
    'random_state': 1,
    'min_samples_split': 2,
    'min_samples_leaf': 1,
    'max_depth': 24,
    'max_features': 40
}

#特征的合并
def merge(a, b, shop):
    fc = lambda x, y: pd.merge(x, y, on='shop_id')
    trade = reduce(fc, a).drop('shop_id', axis=1)
    visit = reduce(fc, b).drop('shop_id', axis=1)

    cat1 = ndarray2df(shop.cate_1_name.values.reshape(2000, 1), 'cat1_')
    cat2 = ndarray2df(shop.cate_2_name.values, 'cat2_')
    cat3 = ndarray2df(shop.cate_3_name.values.reshape(2000, 1), 'cat3_')

    location = ndarray2df(shop.location_id.values.reshape(2000, 1), 'loc_')

    jL = [calcOpenDay(trade), cat1, cat2, cat3, location]
    jL.extend(ExtractMonthFeature())
    jL.extend(ExtractYearFeature())
    jL.extend(ExtractTrainFeature(trade))

    trade['sum'], trade['mean'], trade['median'], \
    trade['max'], trade['min'], trade['var'] = \
        trade.sum(axis=1), trade.mean(axis=1), trade.median(axis=1), \
        trade.max(axis=1), trade.min(axis=1), trade.var(axis=1)

    labelindex = {i: 'visit_{0}'.format(i) for i in visit.columns.values}
    jL.append(visit.rename_axis(labelindex, axis='columns'))

    return reduce(lambda x, y: x.join(y, how='left'), jL)

#线下测试调参
def offlineTest(trade, visit, shop_info, version):
    merge(trade[:2], visit[:2], shop_info).to_csv('../../data/test_train/' + version + 'train_off_x.csv', index=False)
    trade[2:4].drop('shop_id', axis=1).to_csv('../../data/test_train/' + version + 'train_off_y.csv', index=False)

    merge(trade[1:3], visit[1:3], shop_info).to_csv('../../data/test_train/' + version + 'test_off_x.csv', index=False)
    trade[3:5].drop('shop_id', axis=1).to_csv('../../data/test_train/' + version + 'test_off_y.csv', index=False)

    train_off_x, train_off_y = pd.read_csv('../../data/test_train/' + version + 'train_off_x.csv'), pd.read_csv(
        '../../data/test_train/' + version + 'train_off_y.csv')
    test_off_x, test_off_y = pd.read_csv('../../data/test_train/' + version + 'test_off_x.csv'), pd.read_csv(
        '../../data/test_train/' + version + 'test_off_y.csv')

    ET = ExtraTreesRegressor(**params)
    ET.fit(train_off_x, train_off_y)
    features = ET.feature_importances_
    feature_sort = (features / np.sum(features) * 100).round(4)
    feature_index = np.argsort(feature_sort)

    for i in feature_index:
        print('{0} : {1}'.format(train_off_x.columns.values[i], feature_sort[i]))

    ret = ET.predict(test_off_x + 0.5).round()
    print(calcscore(ret, test_off_y.values))

#线上训练预测
def onlineTest(trade, visit, shop_info, version):
    merge(trade[:3], visit[:3], shop_info).to_csv('../../data/test_train/' + version + 'train_on_x.csv', index=False)
    trade[3:5].drop('shop_id', axis=1).to_csv('../../data/test_train/' + version + 'train_on_y.csv', index=False)

    merge(trade[2:5], visit[1:4], shop_info).to_csv('../../data/test_train/' + version + 'test_on_x.csv', index=False)

    train_on_x, train_on_y = pd.read_csv('../../data/test_train/' + version + 'train_on_x.csv'), pd.read_csv(
        '../../data/test_train/' + version + 'train_on_y.csv')
    test_on_x = pd.read_csv('../../data/test_train/' + version + 'test_on_x.csv')

    ET = ExtraTreesRegressor(**params)
    ET.fit(train_on_x, train_on_y)
    A = ET.predict(test_on_x).round()
    pre = repeat_result(A)
    np.savetxt('../../data/results/result_' + version + '.csv',
               np.concatenate((np.arange(1, 2001).reshape(2000, 1), pre), axis=1), delimiter=',',
               fmt='%d')

if __name__ == "__main__":
    version = time.strftime('%Y-%m-%d', time.localtime(time.time())) + '_'
    path = "../../data/weekABCD/"
    trade = [pd.read_csv(path + 'week' + str(i) + '.csv') for i in range(0, 4)] + [pd.read_csv(path + 'weekD.csv')]
    # trade = [pd.read_csv(path + 'week' + chr(i) + '.csv') for i in range(ord('A'), ord('E'))]
    visit = [pd.read_csv(path + 'week' + chr(i) + '_view.csv') for i in range(ord('A'), ord('E'))]
    shop_info = pd.read_csv('../../data/statistics/shop_info_num.csv')

    # 0线下，1线上数据提交
    (offlineTest, onlineTest)[0](trade, visit, shop_info, version)


