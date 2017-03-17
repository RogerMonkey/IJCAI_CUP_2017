# -*- coding: utf-8 -*-
import numpy as np

'''
天气的规则
统计了前21天下雨天占的比例  如果前段时间雨很多，则再晴天提高一定的比例
（具体参数通过2015年统计得到，发现前段时间的天气会影响后面晴天以及雨天的销售量）

雨夹雪 5
中雪 1
中到大雪 2
晴 612
小雪 2
多云 560
雾 12
小到中雨 5
阴 202
小雨 216
霾 46
阵雨 37
小到中雪 2
阵雪 2
中雨 18
'''
def weather_rule(filename, fileto):
    predict = np.loadtxt(filename, delimiter=',')
    weather = []
    ww = {}
    wt = {}
    with open('../../data/statistics/weather-10-11.csv') as f:
        for line in f.readlines():
            item = line.strip().split(',')
            weather.append(item)

    with open('../../data/statistics/weather_city.csv') as f:
        for line in f.readlines():
            item = line.strip().split(',')
            if int(item[0]) not in wt:
                wt[int(item[0])] = float(item[11])

    rate = np.zeros(2000)
    for i in weather:
        rain = 0
        # print(len(i[1:22]))
        for j in i[1:22]:
            if '雨' in j or '雪' in j:
                rain += 1

        rate[int(i[0]) - 1] = rain / 21.0

    # for xx in [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]:
    #     print('{0} rain norain'.format(xx), np.sum(rate <= xx) / rate.shape[0], np.sum(rate >= xx) / rate.shape[0])
    # print('rain in all 3 week:', np.sum(rate > 0.5) / rate.shape[0])
    # print('rain in all 3 week:', np.sum(rate < 0.7) / rate.shape[0])

    for i in weather:
        idx = int(i[0]) - 1
        cdx = 0
        wit = wt[int(i[0])]
        # print(len(i[22:36]))
        for j in i[22:36]:
            cdx += 1
            weight = 1
            if rate[idx] <= 1:
                if '大' in j:
                    weight *= 0.97
                elif '中' in j:
                    weight *= 0.99
                if '雨' in j:
                    weight *= 0.98
                if '雪' in j:
                    weight *= 0.99
                if '霾' in j:
                    weight *= 0.99

            if rate[idx] >= 0.4:  #0.4
                if '晴' in j:
                    weight *= 1.08  # 1.08
                elif '多云' in j:
                    weight *= 1.04  #1.04
                elif '阴' in j:
                    weight *= 1.05  #1.05
                elif '雾' in j:
                    weight *= 1.05  #1.05

            if j not in ww:
                ww[j] = weight
            predict[idx][cdx] *= weight
    np.savetxt(fileto, predict, fmt='%d', delimiter=',')


if __name__ == '__main__':
    pass

