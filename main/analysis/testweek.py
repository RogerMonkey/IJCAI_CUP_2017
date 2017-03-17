__author__ = 'Roger'

# py3 to py2
import numpy as np
import pandas as pd

## analysis and try to find out some rules from the relation between MONTHS and WEE.

# load data and result
result = np.loadtxt('zj/roger_base_test.csv', delimiter=',')
shop = np.loadtxt('shopid_day_num.txt', delimiter=',')
timerange = pd.date_range('2016-1-1', '2016-10-31', freq='D')

weeknum = timerange.weekday
shop = shop[:, -305:]

weekbegin = 3

## cnt for weeks, output the weeks cnt in file
## count the avg of weekdays and weekends
## count the rate of the comparing
with open('als/week/weeks_cnt.txt', 'w') as f:
    f.write('id,end_bigger,end_smaller,end_equal\n')
    print('write to als/week/weeks_cnt.txt')
    all = []
    for i in range(weekbegin, 304, 7):
        weekday_avg = np.mean(shop[:, i:i + 5], axis=1)
        weekend_avg = np.mean(shop[:, i + 5:i + 7], axis=1)
        bigger = np.sum(weekend_avg > weekday_avg) / 2000.0  # the rate of bigger
        smaller = np.sum(weekend_avg < weekday_avg) / 2000.0  # the rate of smaller
        same = np.sum(weekend_avg == weekday_avg) / 2000.0  # the rate of same
        f.write('{0},{1},{2}\n'.format(round(bigger, 2), round(smaller, 2), round(same, 2)))
        if bigger > smaller:
            all.append(i)
    print('rate of bigger weeks:', all.__len__() / (301.0 / 7.0))
    print(all)  # print the biggers

## cnt for weeks, no output
## count the rate between last two weeks and first two weeks every month
## if there is any relation between them

monthnum = timerange.month
first_two_week = np.zeros([2000, 126])
last_two_week = np.zeros([2000, 126])
for i in range(9):
    wk = monthnum == (i + 2)
    first_two_week[:, 14 * i: 14 * (i + 1)] = shop[:, wk][:, 0:14]
    wk = monthnum == (i + 1)
    last_two_week[:, 14 * i: 14 * (i + 1)] = shop[:, wk][:, -14:]

rate = np.zeros([2000, 9])  # init the rate

for i in range(9):
    first_mean = np.mean(first_two_week[:, 14 * i: (i + 1) * 14], axis=1)  # first two weeks' avg
    last_mean = np.mean(last_two_week[:, 14 * i: (i + 1) * 14], axis=1)  # last two weeks' avg
    rate[:, i] = np.mean(first_two_week[:, 14 * i: (i + 1) * 14], axis=1) / np.mean(
        last_two_week[:, 14 * i: (i + 1) * 14], axis=1)

# np.nan_to_num change the inf to the max int which can not easy analysis so that we try to transform by ourselves
for i in range(9):
    for j in range(2000):
        if np.isnan(rate[j, i]):
            rate[j, i] = 0
        if np.isinf(rate[j, i]):
            rate[j, i] = 999

# print the result
print(np.mean(first_two_week[4, 14 * 1: (1 + 1) * 14]))
print(np.mean(last_two_week[4, 14 * 1: (1 + 1) * 14]))
np.savetxt('als/week/last_first_rate.csv', rate, delimiter=',', fmt='%2.4f')

# divide the rate into big and small rate
length = 5
big = rate[:, -1] > 1
small = rate[:, -1] < 1

for i in range(2, 2):
    big = np.logical_and(big, rate[:, -i] > 1)
    small = np.logical_and(small, rate[:, -i] < 1)

print(np.sum(big))
print(np.sum(small))

## analysis two week's relation in first two weeks
for i in range(0, 140, 14):
    first = np.mean(first_two_week[:, i: i + 7], axis=1)
    last = np.mean(first_two_week[:, i + 7: i + 14], axis=1)
    bigger = np.sum(first < last) / 2000.0
    print('month bigger:', bigger)

## analysis if there is any tend between weeks
## include increase and decrease with stable rate or f_l weeks rate
## find out the month which always increase or decrease

bgthen = np.zeros(2000)
lwthen = np.zeros(2000)

for monidx in range(10):
    rate = np.zeros(2000)
    for i in range(2000):
        cnt_inc = 0
        cnt_dec = 0
        for j in range(monidx * 14, 140, 14):
            first = np.mean(first_two_week[i, j: j + 7])
            last = np.mean(first_two_week[i, j + 7: j + 14])
            if first > last:
                cnt_inc += 1
            if first < last:
                cnt_dec += 1
            rate[i] += last  * 1.0/ first

        rate[i] = rate[i] / (10.0 - monidx)
        bgthen[i] = cnt_inc / (10.0 - monidx)
        lwthen[i] = cnt_dec / (10.0 - monidx)

    result[bgthen == 1, -7:] = result[bgthen == 1, 1:-7] * rate[bgthen == 1].reshape(np.sum(bgthen == 1), 1)
    result[bgthen == 0, 1:-7] = result[bgthen == 0, 1:-7] * 0.99

    print('month', monidx + 1, 'f > l always', np.sum(bgthen == 1))
    print('month', monidx + 1, 'f < l always', np.sum(lwthen == 1))
    print('rate f > l', rate[bgthen == 1])

np.savetxt('test/onlydown_with_5month.csv', result, fmt='%d', delimiter=',')

## analysis the tend of weeks
weekbegin = 3
week_mean = np.zeros([2000, 43])
idxw = 0
for i in range(weekbegin, 304, 7):
    week_mean[:, idxw] = np.mean(shop[:, i:i + 7], axis=1)
    for j in range(2000):
        if week_mean[j, idxw] == 0:
            week_mean[j, idxw] = 1
    idxw += 1

week_tend = np.zeros([2000, 43])
for i in range(1, week_mean.shape[1]):
    week_tend[:, i - 1] = week_mean[:, i - 1]  * 1.0/ week_mean[:, i]

week_tend[:, -1] = week_mean[:, -1]  * 1.0/ np.mean(result[:, 1:8])
# weekend_avg = np.mean(shop[:,i+5:i+7], axis=1)

# load the weektend data
np.savetxt('als/week/weektend.csv', week_tend, delimiter=',')

week_part = week_tend[-20:]
print(week_tend)

# output the result for rules test
cntd = 0
cnta = 0
for i in range(2000):
    if week_tend[i, -4] < 1 and week_tend[i, -2] < 1 and week_tend[i, -3] < 1:
        cntd += 1
        result[i, -7:] = result[i, -7:] * 0.98
    if week_tend[i, -2] > 1 and week_tend[i, -3] > 1:
        cnta += 1
        result[i, -7:] = result[i, -7:] * 1.04
print(cntd, cnta)
np.savetxt('test/justbesttest.csv', result, delimiter=',', fmt='%d')
