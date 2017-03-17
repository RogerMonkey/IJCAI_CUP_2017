# -*- coding: utf-8 -*-
import pandas as pd
from datetime import datetime,timedelta

'''
线下测试集和训练集生产
这里线下取了五周ZABCD的数据作为线下测试数据
Z:2016 - 09 - 13 至 2016 - 09-19
A:2016 - 09 - 20 至 2016 - 09-26
B:2016 - 10 - 11 至 2016 - 10 -17
C:2016 - 10 - 18 至 2016 - 10 -24
D:2016 - 10 - 25 至 2016 - 10 -31
'''

#本函数用于将count_user_pay中，列名称全部转变为datetime格式
def transform_count_user_pay_datetime(count_user_pay):
    col = count_user_pay.columns
    tmp = []
    tmp1 = []
    for one in col:
        tmp.append(one.replace('count_user_pay_',''))
    for one in tmp:
        tmp1.append(one.replace('_','-'))
    col = []
    col.append(tmp1[0])
    for one in tmp1[1:]:
        col.append(datetime.strptime(one,'%Y-%m-%d'))
    count_user_pay.columns = col
    return count_user_pay

#本函数用于将count_user_view中，列名称全部转变为datetime格式，并且返回。
def transform_count_user_view_datetime(count_user_view):
    col = count_user_view.columns
    tmp = []
    tmp1 = []
    for one in col:
        tmp.append(one.replace('count_user_view_',''))
    for one in tmp:
        tmp1.append(one.replace('_','-'))
    col = []
    col.append(tmp1[0])
    for one in tmp1[1:]:
        col.append(datetime.strptime(one,'%Y-%m-%d'))
    count_user_view.columns = col
    return count_user_view

def split_week(weekName,num_start_day=0, num_end_day=488, week=False, fr='D'):
    start_day = '2015-07-01'
    start_day = datetime.strptime(start_day, '%Y-%m-%d') + timedelta(days=num_start_day)
    end_day = start_day + timedelta(days=num_end_day - num_start_day)
    dates = pd.date_range(start=start_day, end=end_day, freq=fr)

    try:
        dates = dates.drop(datetime(2015, 12, 12))
    except ValueError:
        print ''

    count_user_pay = pd.read_csv('../../data/statistics/count_user_pay.csv')
    count_user_pay.index = count_user_pay.shop_id.values
    count_user_pay = transform_count_user_pay_datetime(count_user_pay)
    values = count_user_pay.ix[[i for i in range(1,2001)],dates]
    # print values[:]
    values.to_csv('../../data/weekABCD/' + weekName + '.csv')

def split_week_view(weekName,num_start_day=0, num_end_day=488, week=False, fr='D'):
    start_day = '2015-07-01'
    start_day = datetime.strptime(start_day, '%Y-%m-%d') + timedelta(days=num_start_day)
    end_day = start_day + timedelta(days=num_end_day - num_start_day)
    dates = pd.date_range(start=start_day, end=end_day, freq=fr)

    try:
        dates = dates.drop(datetime(2015, 12, 12))
    except ValueError:
        print ''

    count_user_pay = pd.read_csv('../../data/count_pay_and_view/count_user_view.csv')
    count_user_pay.index = count_user_pay.shop_id.values
    count_user_pay = transform_count_user_view_datetime(count_user_pay)
    values = count_user_pay.ix[[i for i in range(1,2001)],dates]
    print values[:]
    values.to_csv('../../data/weekABCD/' + weekName + '.csv')


if __name__ == '__main__':
    #2016 - 9-13 至 2016 - 9-19
    weekName = "weekZ"
    split_week(weekName, num_start_day=440, num_end_day=446)
    #2016 - 9-20 至 2016 - 9-26
    weekName = "weekA"
    split_week(weekName, num_start_day=447, num_end_day=453)
    #2016 - 10 - 11 至 2016 - 10 -17
    weekName = "weekB"
    split_week(weekName, num_start_day=468, num_end_day=474)
    # 2016 - 10 - 18 至 2016 - 10 -24
    weekName = "weekC"
    split_week(weekName, num_start_day=475, num_end_day=481)
    # 2016 - 10 - 25 至 2016 - 10 -31
    weekName="weekD"
    split_week(weekName,num_start_day=482,num_end_day=488)


    weekName = "weekA_view"
    split_week_view(weekName, num_start_day=447, num_end_day=453)
    weekName = "weekB_view"
    split_week_view(weekName, num_start_day=468, num_end_day=474)
    weekName = "weekC_view"
    split_week_view(weekName, num_start_day=475, num_end_day=481)
    weekName="weekD_view"
    split_week_view(weekName,num_start_day=482,num_end_day=488)