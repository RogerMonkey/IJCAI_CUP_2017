__author__ = 'Roger'

import numpy as np

## simple test week for week tend.
## and we find out this is no use in the middle of the game

def find_week(path, data_name, shop, time, analysis_name):
    week_list = ['周一','周二','周三','周四','周五','周六','周日']
    f = open(path + analysis_name, 'w')
    shopdata = shop
    dayofweek = time.dayofweek
    # sum_all_week = np.zeros([2000,7])
    avg_week = np.zeros([2000,7])
    # avg_16_week = np.zeros([,7])
    for i in range(2000):
        for j in range(7):
            # sum_all_week[i,j] = np.sum(shopdata[dayofweek == j,i])
            avg_week[i,j] = np.sum(shopdata[dayofweek == j,i])  * 1.0/ shopdata[dayofweek == j,i].shape[0]

    # np.savetxt('sum_all_week.csv', sum_all_week,delimiter=',', fmt='%d')
    np.savetxt(path + data_name, avg_week,delimiter=',', fmt='%d')

    # mean tend
    f.write('均值趋势分析：\n')
    max_per_week = np.zeros(2000)
    min_per_week = np.zeros(2000)
    for i in range(2000):
        for j in range(7):
            if avg_week[i,j] == np.max(avg_week[i]):
                max_per_week[i] = j
            if avg_week[i,j] == np.min(avg_week[i]):
                min_per_week[i] = j
    print(max_per_week.shape)
    for i in range(7):
        print(np.sum(max_per_week == i))
        f.write('{0}最大的商家有 {1} 个， 占比 {2} %\n'.format(week_list[i], np.sum(max_per_week == i), (np.sum(max_per_week == i) / 2000 * 100).round(2)))

if __name__ == '__main__':
    shop = np.loadtxt('../data/shopid_day_num.txt', delimiter=',')
    print(shop.shape)
    # shop = shop.T
    # time = pd.date_range('2015-7-1', '2016-10-31', name='Date', freq='D')
    # print('2015-7-11' in time)
    # shop = np.concatenate((shop[0:165, :], np.zeros([1, 2000]), shop[165:, :]), axis=0)
    # shop_data = pd.DataFrame(data=shop[1:, :], index=time, columns=range(1, 2001))
    # print(dt.datetime(2016,10,31) - dt.datetime(2016,1,1))
    # find_week('analysis/','all_week_avg.csv',shop[1:,:],time,'all_week_avg.als')
    # find_week('analysis/','16_week_avg.csv',shop[-304:],time[-304:],'16_week_avg.als')
    # find_week('analysis/','last3_week_avg.csv',shop[-21:,:],time[-21:],'last3_week_avg.als')
    # find_week('analysis/','lask5_week_avg.csv',shop[-35:,:],time[-35:],'last5_week_avg.als')
    # series = pd.date_range('2016-10-11', '2016-11-14')
    # print('2016-10-11' in series)
