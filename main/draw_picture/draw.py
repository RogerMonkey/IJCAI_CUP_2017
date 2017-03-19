# -*- coding:utf-8 -*-
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import random
from datetime import datetime, timedelta
import sys

sys.path.append('../main')
from unit import *


# 单个商家客流量的走势图，可调整时间段，也可以按指定的周几绘图
def draw_single_shop(shop_id, num_start_day=0, num_end_day=488, week=False, fr='D'):
    start_day = '2015-07-01'
    start_day = datetime.strptime(start_day, '%Y-%m-%d') + timedelta(days=num_start_day)
    end_day = start_day + timedelta(days=num_end_day - num_start_day)
    dates = pd.date_range(start=start_day, end=end_day, freq=fr)

    try:
        dates = dates.drop(datetime(2015, 12, 12))
    except ValueError:
        print ''

    delta = (end_day - start_day).days
    count_user_pay = pd.read_csv('../../data/statistics/count_user_pay.csv')
    count_user_pay.index = count_user_pay.shop_id.values
    count_user_pay = transform_count_user_pay_datetime(count_user_pay)
    values = count_user_pay.ix[shop_id, dates]
    fig = plt.figure(random.randint(1, 10000))
    ax = fig.add_subplot(111)

    xticklabels_date = values.index
    xticklabels_week = []
    for one in xticklabels_date:
        xticklabels_week.append(one.strftime('%a'))
    if (week):
        xticklabels = xticklabels_week
    else:
        xticklabels = xticklabels_date
    if (delta < 100):
        ax.set_xticks([i for i in range(len(values))])
        ax.set_xticklabels(xticklabels, rotation=-90)
    ax.set_title(
        'shop_id:' + str(shop_id) + '   ' + start_day.strftime('%Y-%m-%d') + ' ~ ' + end_day.strftime('%Y-%m-%d'))
    ax.grid()
    plt.subplots_adjust(bottom=0.2)
    ax.plot(values, label=shop_id)
    ax.legend(loc='best')


# 多个商家客流量的走势图，可调整时间段，也可以按指定的周几绘图，可以计算avg.
def draw_multi_shops(shop_id=[i for i in range(1, 2001)], num_start_day=0, num_end_day=488, week=False, fr='D',
                     _mean=False, _min=False, _std=False, _25=False, _50=False, _75=False, _max=False):
    if (type(num_start_day) == type(num_end_day) == type(1)):
        start_day = '2015-07-01'
        start_day = datetime.strptime(start_day, '%Y-%m-%d') + timedelta(days=num_start_day)
        end_day = start_day + timedelta(days=num_end_day - num_start_day)
    else:
        start_day = datetime.strptime(num_start_day, '%Y-%m-%d')
        end_day = datetime.strptime(num_end_day, '%Y-%m-%d')
    dates = pd.date_range(start=start_day, end=end_day, freq=fr)

    try:
        dates = dates.drop(datetime(2015, 12, 12))
    except ValueError:
        print ''

    delta = (end_day - start_day).days
    count_user_pay = pd.read_csv('../../data/statistics/count_user_pay.csv')
    count_user_pay.index = count_user_pay.shop_id.values
    count_user_pay = transform_count_user_pay_datetime(count_user_pay)
    values = count_user_pay.ix[shop_id, dates]

    fig = plt.figure(num=random.randint(1, 10000))
    ax = fig.add_subplot(111)
    xticklabels_date = values.columns
    xticklabels_week = []
    for one in xticklabels_date:
        xticklabels_week.append(one.strftime('%a'))
    if (week):
        xticklabels = xticklabels_week
    else:
        xticklabels = xticklabels_date

    if (delta < 100):
        ax.set_xticks([i for i in range(len(values.columns))])
        ax.set_xticklabels(xticklabels, rotation=-90)
    ax.set_title('[pay]  ' + start_day.strftime('%Y-%m-%d') + ' ~ ' + end_day.strftime('%Y-%m-%d'))
    ax.grid()
    if (_mean):
        _mean = (values.describe()).ix['mean']
        ax.plot(_mean, label='avg')
    elif (_std):
        _std = (values.describe()).ix['std']
        ax.plot(_std, label='std')
    elif (_min):
        _min = (values.describe()).ix['min']
        ax.plot(_min, label='min')
    elif (_25):
        _25 = (values.describe()).ix['25%']
        ax.plot(_25, label='25%')
    elif (_50):
        _50 = (values.describe()).ix['50%']
        ax.plot(_50, label='50%')
    elif (_75):
        _75 = (values.describe()).ix['75%']
        ax.plot(_75, label='75%')
    elif (_max):
        _max = (values.describe()).ix['max']
        ax.plot(_max, label='max')
    else:
        for i in shop_id:
            ax.plot(values.ix[i], label=str(i))
    plt.subplots_adjust(bottom=0.2)
    ax.legend(loc='best')


# 多个商家浏览量的走势图，可调整时间段，也可以按指定的周几绘图，可以计算avg.
def draw_multi_shops_view(shop_id=[i for i in range(1, 2001)], num_start_day=0, num_end_day=273, week=False, fr='D',
                          _mean=False, _min=False, _std=False, _25=False, _50=False, _75=False, _max=False):
    if (type(num_start_day) == type(num_end_day) == type(1)):
        start_day = '2016-02-01'
        start_day = datetime.strptime(start_day, '%Y-%m-%d') + timedelta(days=num_start_day)
        end_day = start_day + timedelta(days=num_end_day - num_start_day)
    else:
        start_day = datetime.strptime(num_start_day, '%Y-%m-%d')
        end_day = datetime.strptime(num_end_day, '%Y-%m-%d')
    dates = pd.date_range(start=start_day, end=end_day, freq=fr)

    try:
        dates = dates.drop(datetime(2016, 7, 22))
        dates = dates.drop(datetime(2016, 7, 25))
    except ValueError:
        print ''

    delta = (end_day - start_day).days
    count_user_view = pd.read_csv('../../data/statistics/count_user_view.csv')
    count_user_view.index = count_user_view.shop_id.values
    count_user_view = transform_count_user_view_datetime(count_user_view)
    values = count_user_view.ix[shop_id, dates]

    fig = plt.figure(num=random.randint(1, 10000))
    ax = fig.add_subplot(111)
    xticklabels_date = values.columns
    xticklabels_week = []
    for one in xticklabels_date:
        xticklabels_week.append(one.strftime('%a'))
    if (week):
        xticklabels = xticklabels_week
    else:
        xticklabels = xticklabels_date

    if (delta < 100):
        ax.set_xticks([i for i in range(len(values.columns))])
        ax.set_xticklabels(xticklabels, rotation=-90)
    ax.set_title('[view]  ' + start_day.strftime('%Y-%m-%d') + ' ~ ' + end_day.strftime('%Y-%m-%d'))
    ax.grid()
    if (_mean):
        _mean = (values.describe()).ix['mean']
        ax.plot(_mean, label='avg')
    elif (_std):
        _std = (values.describe()).ix['std']
        ax.plot(_std, label='std')
    elif (_min):
        _min = (values.describe()).ix['min']
        ax.plot(_min, label='min')
    elif (_25):
        _25 = (values.describe()).ix['25%']
        ax.plot(_25, label='25%')
    elif (_50):
        _50 = (values.describe()).ix['50%']
        ax.plot(_50, label='50%')
    elif (_75):
        _75 = (values.describe()).ix['75%']
        ax.plot(_75, label='75%')
    elif (_max):
        _max = (values.describe()).ix['max']
        ax.plot(_max, label='max')
    else:
        for i in shop_id:
            ax.plot(values.ix[i], label=str(i))
    plt.subplots_adjust(bottom=0.2)
    ax.legend(loc='best')


'''本函数用于将count_user_pay中，列名称全部转变为datetime格式，并且返回。'''


def transform_count_user_pay_datetime(count_user_pay):
    col = count_user_pay.columns
    tmp = []
    tmp1 = []
    for one in col:
        tmp.append(one.replace('count_user_pay_', ''))
    for one in tmp:
        tmp1.append(one.replace('_', '-'))
    col = []
    col.append(tmp1[0])
    for one in tmp1[1:]:
        col.append(datetime.strptime(one, '%Y-%m-%d'))
    count_user_pay.columns = col
    return count_user_pay


'''本函数用于将count_user_view中，列名称全部转变为datetime格式，并且返回。'''


def transform_count_user_view_datetime(count_user_view):
    col = count_user_view.columns
    tmp = []
    tmp1 = []
    for one in col:
        tmp.append(one.replace('count_user_view_', ''))
    for one in tmp:
        tmp1.append(one.replace('_', '-'))
    col = []
    col.append(tmp1[0])
    for one in tmp1[1:]:
        col.append(datetime.strptime(one, '%Y-%m-%d'))
    count_user_view.columns = col
    return count_user_view


# 画数据的折线图
def draw(filename1, filename2, filename3):
    fr1 = open(filename1)

    index = []
    pre_x = []
    pre_y = []
    for line in fr1.readlines():
        data = line.strip().split(",")
        shop_id = data[0]
        index.append(shop_id)
        x = []
        y = []
        i = 1
        for num in data[1:]:
            x.append(i)
            y.append(int(num))
            i += 1
        pre_x.append(x)
        pre_y.append(y)

    fr2 = open(filename2)
    now_x = []
    now_y = []
    for line in fr2.readlines():
        data = line.strip().split(",")
        shop_id = data[0]
        x = []
        y = []
        i = 1
        for num in data[1:]:
            x.append(i)
            y.append(int(num))
            i += 1
        now_x.append(x)
        now_y.append(y)

    fr3 = open(filename3)
    now_x_avg = []
    now_y_avg = []
    for line in fr3.readlines():
        data = line.strip().split(",")
        shop_id = data[0]
        x = []
        y = []
        i = 1
        for num in data[1:]:
            x.append(i)
            y.append(int(num.split(".")[0]))
            i += 1
        now_x_avg.append(x)
        now_y_avg.append(y)

    # print now_x
    # print now_y
    for i in range(len(index)):
        if pre_y[i] != now_y[i]:
            print index[i]
        plt.figure()
        plt.plot(pre_x[i], pre_y[i], color="red", linewidth=1)
        plt.plot(now_x[i], now_y[i], "b", linewidth=1)
        plt.plot(now_x_avg[i], now_y_avg[i], "g", linewidth=1)
        plt.savefig("../pictures/image/" + index[i] + ".jpg")
        plt.close()


def ali_eval(p1, p2):
    result = (p1 - p2) / (p1 + p2)
    result = np.nan_to_num(result)
    return np.mean(np.abs(result))


def cal_diff(filename1, filename2):
    a = np.loadtxt(filename1, delimiter=',')
    b = np.loadtxt(filename2, delimiter=',')
    import math
    sum = 0
    for i in range(0, a.shape[0]):
        for j in range(1, a.shape[1]):
            sum += math.fabs(a[i, j] - b[i, j]) / (a[i, j] + b[i, j])
    return sum / (a.shape[0] * (a.shape[1] - 1))


if __name__ == '__main__':
    pass
