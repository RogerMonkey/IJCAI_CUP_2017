# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np

"""
########################## 工具函数 #########################
"""


def ndarray2df(arr, column_name='col_'):
    """将一个ndarray转为DataFrame类型"""
    cname = ['col_0'] if len(arr.shape) == 1 else [column_name + str(i) for i in range(arr.shape[1])]
    return pd.DataFrame(arr, columns=cname)


def calc_score(p, d):
    """用于线下测试预测的评分"""
    return np.mean(np.abs(np.nan_to_num((p - d) / (p + d))))


def repeat_result(ret):
    """复制第一周结果接在第一周结果之后，在首列之前加入shop_id列"""
    return np.concatenate((ret, ret), axis=1)

#计算成绩
def calcscore(p, d):
    return np.mean(np.abs(np.nan_to_num((p - d) / (p + d))))

"""
########################## 特征抽取 ################
"""

#获取训练三周对应的特征，包括每周的平均值，相对于前一天的幅度
def ExtractTrainFeature(train):
    Rng, weekAvg = [], []
    for i in range(len(train)):
        d, tot, num = train.ix[i, :], np.zeros(7), np.zeros(7)
        Rng.append([100 if int(d[j - 1]) == 0 else d[j] / d[j - 1] for j in range(1, len(d))])
        for j in range(len(d)):
            if d[j] > 0:
                tot[j % 7] += d[j]
                num[j % 7] += 1
        weekAvg.append([tot[k] / num[k] if num[k] else 1 for k in range(7)])
    return ndarray2df(np.asarray(Rng), 'Rng_'), \
           ndarray2df(np.asarray(weekAvg), 'weekAvg_')


def visit2buy():
    a = np.loadtxt('./data/back.csv', delimiter=',', dtype=np.float64)
    return ndarray2df(a[:, 1].reshape(2000, 1), 'back_')


def repeatRet(ret):
    return np.concatenate((np.arange(1, 2001).reshape(2000, 1), ret, ret), axis=1)

#计算开业率
def calcOpenDay(train):
    return ndarray2df(np.where(train.ix[:, :] > 0, 1, 0), 'openDay_')


#获取最后一个月（除了10月1号一星期的数据）的平均值，求和以及中位数
def ExtractMonthFeature():
    shop = np.loadtxt('../../data/statistics/count_user_pay_avg_no_header.csv', delimiter=',').T
    dateRange = pd.date_range('2016-3-1', '2016-10-31', freq='D', name='Date')
    shop = pd.DataFrame(data=shop[-245:, :], index=dateRange, columns=range(1, 2001))
    monthSum = ndarray2df(shop.ix['2016-10-8':'2016-10-31'].sum(axis=0).values.reshape(2000, 1), 'monthsum_')
    monthMean = ndarray2df(shop.ix['2016-10-8':'2016-10-31'].mean(axis=0).values.reshape(2000, 1), 'monthmean_')
    monthMedian = ndarray2df(shop.ix['2016-10-8':'2016-10-31'].median(axis=0).values.reshape(2000, 1), 'monthmedian_')
    return monthSum, monthMean, monthMedian

#获取每一个月方差，平均值和中位数  每星期之间的方法和每星期的浮动 多个月整体的sum，median和mean
def ExtractYearFeature():
    shop = np.loadtxt('../../data/statistics/count_user_pay_avg_no_header.csv', delimiter=',').T
    dateRange = pd.date_range('2016-3-1', '2016-10-31', freq='D', name='Date')
    shop = pd.DataFrame(data=shop[-245:, :], index=dateRange, columns=range(1, 2001))
    yearVar, yearRng = np.zeros((2000, 7)), np.zeros((2000, 6))
    tmp = shop.ix['2016-3-1':'2016-9-26'].values
    for i in range(2000):
        tw = tmp[:, i].reshape(30, 7)
        yearVar[i, :] = np.var(tw, axis=0)
        avg = np.mean(tw, axis=0)
        for j in range(1, 7):
            yearRng[i, j - 1] = 10 if int(avg[j - 1]) == 0 else avg[j] / avg[j - 1]
    yearMedian, yearAvg = np.zeros((2000, 8)), np.zeros((2000, 8))
    for i, m in enumerate(('31', '30', '31', '30', '31', '31', '30', '31')):
        tmp = shop.ix['2016-' + str(i + 3) + '-1':'2016-' + str(i + 3) + '-' + m]
        yearMedian[:, i] = tmp.median(axis=0).values
        yearAvg[:, i] = tmp.mean(axis=0).values

    yearMRng = np.zeros((2000, 8))
    for i in range(2000):
        for j in range(1, 8):
            yearMRng[i, j - 1] = 10 if int(yearAvg[i, j - 1]) == 0 else yearAvg[i, j] / yearAvg[i, j - 1]

    yearMax = shop.ix['2016-3-1':'2016-10-30'].max(axis=0).values.reshape(2000, 1)
    yearMin = shop.ix['2016-3-1':'2016-10-30'].min(axis=0).values.reshape(2000, 1)
    yearStd = shop.ix['2016-3-1':'2016-10-30'].std(axis=0).values.reshape(2000, 1)

    return ndarray2df(yearMedian, 'yearMedian_'), \
           ndarray2df(yearMax, 'yearMax_'), \
           ndarray2df(yearMin, 'yearMin_'), \
           ndarray2df(yearStd, 'yearStd_'), \
           ndarray2df(yearVar, 'yearVar_'), \
           ndarray2df(yearRng, 'yearRng'), \
           ndarray2df(yearMRng, 'yearMRng_')

def calc_open_day(train):
    """将有交易的天设置为1，没有交易的天设置为0"""
    return ndarray2df(np.where(train.ix[:, :] > 0, 1, 0), 'open_day_')


def open_ratio(threshold=0, start=0, end=488, bigger=True):
    """计算开业率"""
    count_user_pay = pd.read_csv('../../data/statistics/count_user_pay.csv')
    open_ratio_arr, tot = [], end - start + 1
    for row in range(len(count_user_pay)):
        shop = count_user_pay.ix[row][start:end]
        open_ratio_arr.append(round((shop > 0).sum() / tot, 4))
    open_ratio_arr = np.asarray(open_ratio_arr)
    index = bigger and open_ratio_arr >= threshold or open_ratio_arr <= threshold
    return pd.DataFrame({'shop_id': (count_user_pay.shop_id)[index].values, 'open_ratio': open_ratio_arr[index]})


def basic_feature(train):
    """基本统计量"""
    return train.sum(axis=1), train.mean(axis=1), train.median(axis=1), \
           train.max(axis=1), train.min(axis=1), train.var(axis=1), \
           train.std(axis=1), train.mad(axis=1)


def week_ratio_feature(train, train_sum, week, weekend):
    """每周7天的特征"""
    fc = lambda x: train[x].sum(axis=1) / train_sum.replace(0, 1)
    for i, day in enumerate(week):
        for j in range(len(day)):
            day[j] = day[j][:-2] + str(int(day[j][-2:]) + i)
    ratio_tues, ratio_wed, ratio_thurs, ratio_fri, ratio_sat, ratio_sun, ratio_mon = list(map(fc, week))
    ratio_wk = (train[weekend]).sum(axis=1) / (train_sum.replace(0, 1))
    return ratio_mon, ratio_tues, ratio_wed, ratio_thurs, ratio_fri, ratio_sat, ratio_sun, ratio_wk


def global_day_feature(data, index=-61):
    """全局数据按天基本统计量"""
    return data.ix[:, index:].sum(axis=1), data.ix[:, index:].mean(axis=1), \
           data.ix[:, index:].median(axis=1), data.ix[:, index:].max(axis=1), \
           data.ix[:, index:].var(axis=1), data.ix[:, index:].std(axis=1), \
           data.ix[:, index:].mad(axis=1)


def global_month_feature(data):
    """全局数据按月基本统计量"""
    month_sum, month_average, month_median, months = [], [], [], [31, 30, 31]
    month_max, month_min, month_std, month_var = [], [], [], []
    for i in range(1, len(months)):
        months[i] += months[i - 1]

    for i in range(len(data)):
        data_ = data.ix[i, :].values
        month_sum_, month_average_, month_median_, month_max_, month_min_, month_std_, month_var_ = list(
            map(lambda f: f(data_[-months[0]:]), [np.sum, np.mean, np.median, np.max, np.min, np.std, np.var]))
        for j in range(1, len(months)):
            d = data_[-months[j]:-months[j - 1]]
            month_average_.insert(0, np.mean(d))
            month_sum_.insert(0, np.sum(d))
            month_median_.insert(0, np.median(d))
            month_max_.insert(0, np.max(d))
            month_min_.insert(0, np.min(d))
            month_std_.insert(0, np.std(d))
            month_var_.insert(0, np.var(d))

        month_average.append(month_average_)
        month_sum.append(month_sum_)
        month_median.append(month_median_)
        month_max.append(month_max_)
        month_min.append(month_min_)
        month_std.append(month_std_)
        month_var.append(month_var_)

    return ndarray2df(np.asarray(month_sum), 'month_sum_'), \
           ndarray2df(np.asarray(month_average), 'month_avg_'), \
           ndarray2df(np.asarray(month_median), 'month_median_'), \
           ndarray2df(np.asarray(month_max), 'month_max_'), \
           ndarray2df(np.asarray(month_min_), 'month_min_'), \
           ndarray2df(np.asarray(month_std), 'month_std_'), \
           ndarray2df(np.asarray(month_var), 'month_var_')


def day_feature(data):
    """相邻天的差值以及周内各天的均值"""
    diff, day_avg = [], []
    for i in range(len(data)):
        d = data.ix[i, :].values
        diff.append([d[j] - d[j - 1] for j in range(1, len(d))])
        sum_, tot_ = np.zeros(7), np.zeros(7)
        for j in range(len(d)):
            sum_[j % 7] += d[j]
            tot_[j % 7] += int(d[j] > 0)
        day_avg.append([sum_[j] / tot_[j] if tot_[j] else 0 for j in range(7)])
    return ndarray2df(np.asarray(diff), 'diff_'), ndarray2df(np.asarray(day_avg), 'seven_day_')


def week_basic_feature(data):
    """每周的基本统计量"""
    week_sum, week_avg, week_median = [], [], []
    week_max, week_min, week_std, week_var = [], [], [], []
    for i in range(len(data)):
        d = data.ix[i, :].values
        arr = [d[:7], d[7:]]
        week_avg.append(list(map(np.mean, arr)))
        week_sum.append(list(map(np.sum, arr)))
        week_median.append(list(map(np.median, arr)))
        week_max.append(list(map(np.max, arr)))
        week_min.append(list(map(np.min, arr)))
        week_std.append(list(map(np.std, arr)))
        week_var.append(list(map(np.var, arr)))

    return ndarray2df(np.asarray(week_sum), 'week_sum_'), \
           ndarray2df(np.asarray(week_avg), 'week_avg_'), \
           ndarray2df(np.asarray(week_median), 'week_median_'), \
           ndarray2df(np.asarray(week_max), 'week_max_'), \
           ndarray2df(np.asarray(week_min), 'week_min_'), \
           ndarray2df(np.asarray(week_std), 'week_std_'), \
           ndarray2df(np.asarray(week_var), 'week_var_')


def calc_open_ratio():
    """计算开业率"""
    return 0.5 * (open_ratio(start=447, end=453).open_ratio + open_ratio(start=468, end=474).open_ratio)


def shop_cate_feature(shop):
    """shop类型特征"""
    return ndarray2df(shop.cate_1_name.values.reshape(2000, 1), 'cat1_'), \
           ndarray2df(shop.cate_2_name.values.reshape(2000, 1), 'cat2_'), \
           ndarray2df(shop.cate_3_name.values.reshape(2000, 1), 'cat3_')


def shop_location_feature(shop):
    """商店location_id特征"""
    return ndarray2df(shop.location_id.values.reshape(2000, 1), 'loc_')


def calcWeekGainRate(train):
    """计算训练集中相邻周的总交易量的比率"""
    weekGainRate = []
    for i in range(len(train)):
        d = train.ix[i, :]
        Gain = []
        for j in range(1, int(len(d) / 7)):
            a, b = sum(d.values[(j - 1) * 7:j * 7]), sum(d.values[j * 7:(j + 1) * 7])
            Gain.append(b / a if a > 0 else 1)
        weekGainRate.append(Gain)
    return ndarray2df(np.asarray(weekGainRate), 'weekGainRate_')



if __name__ == '__main__':
    pass


