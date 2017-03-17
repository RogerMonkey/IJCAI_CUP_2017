__author__ = 'Roger'

import copy
import warnings

import pandas as pd
from statsmodels.tsa.arima_model import ARMA
from test import test_stationarity

from prepare import *

## some little tools for fast test and model
## we define grid searh for model model and predict
## eval with bic or smape
warnings.filterwarnings('ignore')

P_range = [0, 1, 2, 3, 4, 5, 6, 7]
Q_range = [0, 1, 2, 3, 4, 5, 6, 7]


## common eval
def ali_eval(correct, predict):
    answer = (correct - predict)  * 1.0/ (correct + predict)
    answer = np.nan_to_num(answer)
    return np.sum(np.fabs(answer))  * 1.0/ answer.shape[0]


## ARIMA eval
def bic(shop_series, results_ARMA):
    return results_ARMA.bic


def eval1(shop_series, results_ARMA):
    index = shop_series.values.shape[0] // 2
    correct = shop_series.values[-index:]
    predict = results_ARMA.predict().values[-index:]
    return ali_eval(correct, predict)


def eval2(shop_series, results_ARMA):
    correct = shop_series.values
    predict = results_ARMA.forecast(14)[0]
    # print(predict)

    return ali_eval(correct, predict)


## difference
def find_best_one_step(series):
    for i in range(14):
        tmp = one_step_diff(series, i)
        if test_stationarity(tmp):
            return i

    return 0


## one step difference
def one_step_diff(series, d=0):
    if d == 0:
        return series
    size = series.shape[0]
    result = copy.deepcopy(series)
    for i in range(size - 1, d - 1, -1):
        result[i] = result[i] - result[i - d]

    return result


## one step diff recover
def one_step_recover(series, d=0):
    if d == 0:
        return series
    size = series.shape[0]
    result = copy.deepcopy(series)
    for i in range(d, size):
        result[i] = result[i] + result[i - d]

    return result


## load data
def load_data_and_create_series(begin_time, days):
    index, shop = load_data_as_npdict()

    # TODO: pre process data
    pd_index = pd.date_range(begin_time, periods=days)

    shop_series_list = {}

    for i in shop:
        # TODO: series analysis
        if i not in shop_series_list:
            train = shop[i][-days:]
            train_mean = np.mean(train)
            for it in range(days):
                if train[it] > train_mean * 5 or train[it] < train_mean * 0.05:
                    train[it] = train_mean
            shop_series_list[i] = pd.Series(train, index=pd_index, dtype='f')
    return shop_series_list


def find_best_model(shop_series, eval):
    init_value = 999999999
    best_p = 0
    best_q = 0
    best_model = None

    # simple cutdown
    if eval == eval2:
        train = shop_series[:-14]
        test = shop_series[-14:]
    else:
        train = shop_series
        test = shop_series

    ################
    train = np.log(train)
    d = find_best_one_step(train)
    train = one_step_diff(train, d)
    ################
    for p in P_range:
        for q in Q_range:
            try:
                model = ARMA(train[d:], order=(p, q))  # TODO: ARIMA zero problem
                results_ARMA = model.fit(disp=-1, method='css')
                value = eval(test, results_ARMA)
                # print(value)
                if value < init_value:
                    best_p = p
                    best_q = q
                    init_value = value
            except:
                # print("something wrong!")
                continue

    print(d, best_p, best_q, init_value)
    best_model = ARMA(train[d:], order=(best_p, best_q))
    best_model = best_model.fit(disp=-1, method='css')
    return d, init_value, train, best_model


def find_all_best_model(shop_series_list, eval=bic):
    value = 0
    sum = 0
    best_model_list = {}
    for id in shop_series_list:
        print('find {0}th model:'.format(id))
        d, init_value, train, best_model = find_best_model(shop_series_list[id], eval)
        value += init_value
        sum += 1
        if best_model is not None:
            # best_model_list[id] = best_model
            result = best_model.predict('2016-11-1', '2016-11-14', dynamic=True)
            result = np.append(train.values, result.values)
            print(result)
            result = one_step_recover(result, d)
            print(result)
            result = np.exp(result)
            best_model_list[id] = result[-14:]
        else:
            print('Ouch!')
        print('mean lost: {0}'.format(value * 1.0 / sum))
    return best_model_list


# discard
def predict_result(best_model_list):
    result_list = {}
    for id in best_model_list:
        # result = best_model_list[id].predict('2016-11-1', '2016-11-14', dynamic=True)
        # result_list[id] = result.values
        result = best_model_list[id].forecast(28)[0]
        result_list[id] = result[-14:]
        print(result[-14:])
    return result_list


def save_result(result_list):
    f = open('predict_arma_61_os_bic.csv', 'w')
    for i in result_list:
        r = [int(x) for x in result_list[i]]
        for index in range(r.__len__()):
            if r[index] < 0:
                r[index] = 0
        s = ','.join([str(x) for x in r])
        f.write('{0},{1}\n'.format(i, s))


if __name__ == '__main__':
    shop_series_list = load_data_and_create_series('2016-9-1', 61)
    # count_stationaryity(shop_series_list,7)
    for i in range(20, 2000):
        shop_series_list.pop(i)
    best_model_list = find_all_best_model(shop_series_list, eval=bic)
    # result_list = predict_result(best_model_list)
    #
    save_result(best_model_list)
