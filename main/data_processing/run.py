# -*- coding: utf-8 -*-
from avg_smoothing import *
from smoothing import *
from split_test_train import *

def run():

    '''
    avg_smoothing
    :return:
    '''
    filename = "../../data/statistics/count_user_pay.csv"
    fileto = "../../data/statistics/count_user_pay_avg.csv"
    cal_avg(filename, fileto, 123)

    '''
    smoothing
    '''
    get_static_week()
    data1 = pd.read_csv('./week_output.csv', names=range(0, 15))
    standardDF = data1.ix[:, 1:7]
    # print standardDF.shape
    data2 = pd.read_csv('../../data/statistics/shop_day_num.txt', names=range(0, 495))
    week4(data2, standardDF)
    week3(data2, standardDF)
    week2(data2, standardDF)
    week1(data2, standardDF)
    week0(data2, standardDF)

    '''
    split_test_train
    '''
    # 2016 - 9-13 至 2016 - 9-19
    weekName = "weekZ"
    split_week(weekName, num_start_day=440, num_end_day=446)
    # 2016 - 9-20 至 2016 - 9-26
    weekName = "weekA"
    split_week(weekName, num_start_day=447, num_end_day=453)
    # 2016 - 10 - 11 至 2016 - 10 -17
    weekName = "weekB"
    split_week(weekName, num_start_day=468, num_end_day=474)
    # 2016 - 10 - 18 至 2016 - 10 -24
    weekName = "weekC"
    split_week(weekName, num_start_day=475, num_end_day=481)
    # 2016 - 10 - 25 至 2016 - 10 -31
    weekName = "weekD"
    split_week(weekName, num_start_day=482, num_end_day=488)

    weekName = "weekA_view"
    split_week_view(weekName, num_start_day=447, num_end_day=453)
    weekName = "weekB_view"
    split_week_view(weekName, num_start_day=468, num_end_day=474)
    weekName = "weekC_view"
    split_week_view(weekName, num_start_day=475, num_end_day=481)
    weekName = "weekD_view"
    split_week_view(weekName, num_start_day=482, num_end_day=488)