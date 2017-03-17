__author__ = 'Roger'
## from py3 to py2
import numpy as np

## save median, var, std
shop = np.loadtxt('../data/shopid_day_num.txt', delimiter=',')

all = shop[:, -21:]

week3 = shop[:, -7:]

month = shop[:, -14:]

res = np.zeros([2000, 13])

res[:, 0] = shop[:, 0]
res[:, 1] = np.mean(all, axis=1)
res[:, 2] = np.mean(month, axis=1)
res[:, 3] = np.mean(week3, axis=1)
res[:, 4] = np.median(all, axis=1)
res[:, 5] = np.median(month, axis=1)
res[:, 6] = np.median(week3, axis=1)
res[:, 7] = np.var(all, axis=1)
res[:, 8] = np.var(month, axis=1)
res[:, 9] = np.var(week3, axis=1)
res[:, 10] = np.std(all, axis=1)
res[:, 11] = np.std(month, axis=1)
res[:, 12] = np.std(week3, axis=1)

np.savetxt('../data/all_mon_week3_mean_med_var_std.csv', res, delimiter=',', fmt='%d')
