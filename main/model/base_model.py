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
    train AB->C
    test  BC->D
3.线上onlineTest
    train ABC->D
    test  BCD
4.使用ExtraTreesRegressor 连续预测7天数值，第二星期复制

使用的主要特征有：
1.商店的laction，三级cate
2.前三星期每天的流量
3.用户的浏览记录
4.三周整体的sum,mean,median,max,min,var,std
5.前三周每周一，每周二...,每周日的平均值
5.三星期每星期的sum,mean,median,max,min,var,std
6.三星期每星期相对于前面一天的浮动
7.前五个月整体的sum,mean,median,max,min,var,std
8.前五个月每个月的sum,mean,median,max,min,var,std
9.前五个月每星期相对于前一个星期的浮动
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

    cate = shop_cate_feature(shop)

    jL = [calcOpenDay(trade), cate, shop_location_feature(shop)]
    jL.extend(ExtractMonthFeature())
    jL.extend(ExtractYearFeature())
    jL.extend(ExtractTrainFeature(trade))
    # jL.extend(calcWeekGainRate(trade))
    # jL.extend(week_basic_feature(trade))

    trade['sum'], trade['mean'], trade['median'], \
    trade['max'], trade['min'], trade['var'],trade['std'], trade['mad']= basic_feature(trade)
    #
    all_data = pd.read_csv('../../data/statistics/count_user_pay.csv')
    trade['Allsum'], trade['Allmean'], trade['Allmedian'], \
    trade['Allmax'], trade['Allvar'], trade['Allstd'], trade['Allmad'] = global_day_feature(all_data)
    # jL.extend(global_month_feature(all_data))
    # jL.extend(global_day_feature(all_data))
    # jL.extend(day_feature(all_data))

    labelindex = {i: 'visit_{0}'.format(i) for i in visit.columns.values}
    jL.append(visit.rename_axis(labelindex, axis='columns'))

    return reduce(lambda x, y: x.join(y, how='left'), jL)

#线下测试调参
def offlineTest(trade, visit, shop_info, version):
    merge(trade[:2], visit[:2], shop_info).to_csv('../../data/test_train/' + version + 'train_off_x.csv', index=False)
    trade[2].drop('shop_id', axis=1).to_csv('../../data/test_train/' + version + 'train_off_y.csv', index=False)

    merge(trade[1:3], visit[1:3], shop_info).to_csv('../../data/test_train/' + version + 'test_off_x.csv', index=False)
    trade[3].drop('shop_id', axis=1).to_csv('../../data/test_train/' + version + 'test_off_y.csv', index=False)

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
    print(calc_score(ret, test_off_y.values))

#线上训练预测
def onlineTest(trade, visit, shop_info, version):
    trade[3] = pd.read_csv(path + 'week4.csv')
    merge(trade[:3], visit[:3], shop_info).to_csv('../../data/test_train/' + version + 'train_on_x.csv', index=False)
    trade[3].drop('shop_id', axis=1).to_csv('../../data/test_train/' + version + 'train_on_y.csv', index=False)

    merge(trade[1:4], visit[1:4], shop_info).to_csv('../../data/test_train/' + version + 'test_on_x.csv', index=False)

    train_on_x, train_on_y = pd.read_csv('../../data/test_train/' + version + 'train_on_x.csv'), pd.read_csv(
        '../../data/test_train/' + version + 'train_on_y.csv')
    test_on_x = pd.read_csv('../../data/test_train/' + version + 'test_on_x.csv')

    ET = ExtraTreesRegressor(**params)
    ET.fit(train_on_x, train_on_y)
    A = ET.predict(test_on_x).round()
    pre = repeat_result(A)
    np.savetxt('../../data/results/result_' + version + '.csv', np.concatenate((np.arange(1, 2001).reshape(2000, 1), pre), axis=1), delimiter=',',
               fmt='%d')

if __name__ == "__main__":
    version = time.strftime('%Y-%m-%d', time.localtime(time.time())) + '_'
    path = "../../data/weekABCD/"
    trade = [pd.read_csv(path + 'week' + str(i) + '.csv') for i in range(1, 4)] + [pd.read_csv(path + 'weekD.csv')]
    # trade = [pd.read_csv(path + 'week' + chr(i) + '.csv') for i in range(ord('A'), ord('E'))]
    visit = [pd.read_csv(path + 'week' + chr(i) + '_view.csv') for i in range(ord('A'), ord('E'))]
    shop_info = pd.read_csv('../../data/statistics/shop_info_num.csv')

    # 0线下，1线上数据提交
    (offlineTest, onlineTest)[0](trade, visit, shop_info, version)
    (offlineTest, onlineTest)[1](trade, visit, shop_info, version)


