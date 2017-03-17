__author__ = 'Roger'

import product
import numpy as np

## simple test with average
base_path = "../../../data/"
data = np.loadtxt(base_path + 'statistics/shopid_day_num.txt', delimiter=',')
best_day = [0, 0, 0]
best_score = 99999999

## ignore guoqing and zero
tmp = np.zeros([2000, 28])
for i in range(2000):
    sum = 1
    for j in range(1, data.shape[1]):
        if sum > 28:
            continue
        if data[i][-j] != 0:
            tmp[i][-sum] = data[i][-j]
            sum += 1

data = tmp[:, -21:]
train = tmp[:, :-7]
test = tmp[:, -7:]

for day_21 in np.arange(0, 1, 0.01):
    for day_14 in np.arange(0, 1 - day_21, 0.01):
        tmp_rlt = np.zeros([data.shape[0], 7])
        for j in range(0, 7):
            tmp_rlt[:, j] = train[:, j - 1] * day_21 + train[:, 6 + j] * day_14 + train[:, 13 + j] * (
                1 - day_21 - day_14)
            value = product.ali_eval(test, tmp_rlt)
            if value < best_score:
                best_score = value
                best_day = [day_21, day_14, 1 - day_21 - day_14]

print(best_day, best_score)

result = np.zeros([data.shape[0], 15])

## last 21days every 7 sum
for i in range(2000):
    result[i, 0] = i + 1

for j in range(1, 8):
    result[:, j] = data[:, j - 1] * best_day[0] + data[:, 6 + j] * best_day[1] + data[:, 13 + j] * best_day[2]
    result[:, 7 + j] = result[:, j]

np.savetxt(base_path + 'results/result_avg7_common_with_last_week.csv', result, delimiter=',', fmt='%d')
