__author__ = 'Roger'

import numpy as np
import pandas as pd

## analysis the weather to find if there is any rules
## count the weather with good or bad
## and then try to more concrete analysis

## count the weather from 10-11 to 11-14
def count_wtr():
    time = pd.date_range('2016-10-11','2016-11-14')
    weather = {}
    wind = {}
    shop_info = {}
    # load shop info
    with open('../data/shop_info.txt') as f:
        for line in f.readlines():
            item = line.strip().split(',')
            if int(item[0]) not in shop_info:
                shop_info[item[0]] = {}
            shop_info[item[0]]['city'] = item[1]

    # load city weather and create the weather dict
    with open('city_weather.csv') as f:
        for line in f.readlines():
            item = line.strip().split(',')
            if item[1] not in time:
                continue
            item[4] = item[4].replace('转','-').replace('~','-')
            if item[4] not in weather:
                weather[item[4]] = 0
            weather[item[4]] += 1
            for i in shop_info:
                if item[0] == shop_info[i]['city']:
                    shop_info[i][item[1]] = item[4]

    print(weather.__len__())
    print(sum(weather.values()))
    # print the weather
    for w in weather:
        print(w, weather[w])

    date = np.vectorize(lambda s: s.strftime('%Y-%m-%d'))(time.to_pydatetime())
    # save weather data
    with open('weather-10-11.csv', 'w') as f:

        for i in range(1,2001):
            f.write('{0}'.format(i))
            for j in date:
                f.write(',{0}'.format(shop_info[str(i)][j]))
            f.write('\n')
    for w in wind:
        print(w, wind[w])


## count the weather data of predict days 2016-11-01 to 2016-11-14
## to find out if there is any inflect to predict

def cnt_weather_predict_day():
    # load weather data
    weather = open('data/weather-11-14.csv')
    weather_cnt = {}
    for line in weather.readlines():
        item = line.strip().split(',')
        id = int(item[0])
        if id not in weather_cnt:
            weather_cnt[id] = []
        for k in item[1:]:
            weather_cnt[id].append(k)
    # count for day 11-11, 11-12 11-14
    day_special = []
    for id in weather_cnt:
        print('{0}\t{1}\t{2}'.format(weather_cnt[id][-4], weather_cnt[id][-3], weather_cnt[id][-1]))
        day_special.append([weather_cnt[id][-4], weather_cnt[id][-3], weather_cnt[id][-1]])

    # count for 11-11 11-12 11-14
    day = [11, 12, 14]
    for j in [0, 1, 2]:
        cnt_sunny = 0
        cnt_yin = 0
        cnt_dy = 0
        cnt_rain = 0
        for i in day_special:
            # print(i[j])
            if '晴' in i[j]:
                cnt_sunny += 1
            if '雨' in i[j] or '雪' in i[j]:
                cnt_rain += 1
            if '多云' in i[j]:
                cnt_dy += 1
            if '阴' in i[j]:
                cnt_yin += 1

        print(day[j], cnt_sunny, cnt_rain, cnt_dy, cnt_yin)

## analysis the rate between rain and no rain
cnt_weather_predict_day()
predict = np.loadtxt('../res/result_3_1_base_rule_100_features_15_40_2_avg_123.csv',delimiter=',')
weather_list = []
weather_tmp = {}

with open('weather-10-11.csv') as f:
    for line in f.readlines():
        item = line.strip().split(',')
        weather_list.append(item)

with open('als/weather/weather_city.csv') as f:
    for line in f.readlines():
        item = line.strip().split(',')
        if int(item[0]) not in weather_tmp:
            weather_tmp[int(item[0])] = float(item[11])

print(weather_list)
print(weather_tmp)

## analysis the rate of last 3 weeks
rate = np.zeros(2000)
for i in weather_list:
    rain = 0
    # print(len(i[1:22]))
    for j in i[1:22]:
        if '雨' in j or '雪' in j:
            rain += 1
    rate[int(i[0]) - 1] = rain / 21.0
for xx in [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]:
    print('{0} rain norain'.format(xx), np.sum(rate <= xx) * 1.0 / rate.shape[0], np.sum(rate >= xx) / rate.shape[0])
print('rain in all 3 week:', np.sum(rate > 0.5) * 1.0 / rate.shape[0])
print('rain in all 3 week:', np.sum(rate < 0.7) * 1.0 / rate.shape[0])


## find out the shop that inflected by weather

# shop04 = predict[rate >= 0.4, 0]
# shop05 = predict[rate >= 0.5, 0]
#
# print(shop04.shape, shop05.shape)
#
# extsamelist = {}
# for i in shop04:
#     extsamelist[i] = 1
#     for j in shop05:
#         if i == j:
#             extsamelist.pop(i)
#
# print(extsamelist.__len__())
#
# np.savetxt('final/final_not_same_4_5.csv', np.array(list(extsamelist.keys())), fmt='%d', delimiter=',')
# np.savetxt('final/final_shop4.csv', shop04, fmt='%d', delimiter=',')
# np.savetxt('final/final_shop5.csv', shop05, fmt='%d', delimiter=',')


'''
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
