# -*- coding: utf-8 -*-
from base_model import *
from gbdt import *
from RandomForestRegreessor import *
from use_first_week_predict_second_week import *

def run():
    '''
    base_model
    :return:
    '''
    version = time.strftime('%Y-%m-%d', time.localtime(time.time())) + '_'
    path = "../../data/weekABCD/"
    trade = [pd.read_csv(path + 'week' + str(i) + '.csv') for i in range(1, 4)] + [pd.read_csv(path + 'weekD.csv')]
    # trade = [pd.read_csv(path + 'week' + chr(i) + '.csv') for i in range(ord('A'), ord('E'))]
    visit = [pd.read_csv(path + 'week' + chr(i) + '_view.csv') for i in range(ord('A'), ord('E'))]
    shop_info = pd.read_csv('../../data/statistics/shop_info_num.csv')

    # 0线下，1线上数据提交
    (offlineTest, onlineTest)[0](trade, visit, shop_info, version)
    (offlineTest, onlineTest)[1](trade, visit, shop_info, version)

    '''
    GBDT
    '''
    gbdt()

    '''
    RF
    '''
    RF()