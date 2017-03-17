__author__ = 'Roger'

import numpy as np
from sklearn import linear_model

## this is the base test for linear model to predict linear model
## we consider about the increasing model to transform our model
base_path = "../../../data/statistics/"


# def eval
def eval(cor, pdt):
    answer = (cor - pdt)  * 1.0/ (cor + pdt)
    answer = np.nan_to_num(answer)
    return np.sum(np.fabs(answer)) * 1.0 / answer.shape[0]


# load data
def load_data():
    data = np.loadtxt(base_path + 'shopid_day_num.txt', delimiter=',')
    return data[:, 1:]


# sum data
def process_data(data):
    result = np.zeros(data.shape)
    result[0] = data[0]
    for i in range(1, data.shape[0]):
        result[i] = data[i] + result[i - 1]
    return result


# transform the sum data to real data
def rereal_data(base, data):
    result = np.zeros(data.shape)
    result[0] = data[0] - base
    for i in range(1, data.shape[0]):
        result[i] = data[i] - data[i - 1]
    return result


# predict with Ridge
def predict(alphas, offset, d):
    reg = linear_model.RidgeCV(alphas=alphas)
    data = process_data(d)
    train = data[:-offset]
    test = d[-offset:]
    x = np.linspace(1, data.shape[0], data.shape[0])

    reg.fit(x[:-offset, None], train)
    result = reg.predict(x[-offset:, None])

    r = rereal_data(result[0], result)
    return eval(r[1:], test[1:])


# predict for all
def predict_all(alphas, offset, d):
    sum = 0
    for i in range(d.shape[0]):
        sum += predict(alphas, offset, d[i])

    return sum  * 1.0/ d.shape[0]


# test
if __name__ == '__main__':
    par = [0.1, 0.2, 0.3, 0.4, 0.5, 1, 5, 10]
    data = load_data()
    # predict(par,14, data[0,-offset:])
    best_result = 9999
    best_offset = 0
    for offset in range(1, 92):
        re_of = offset + 14
        re = predict_all(par, 14, data[:, -re_of:])
        if re < best_result:
            best_result = re
            best_offset = offset

    print(best_offset)
    print(best_result)
