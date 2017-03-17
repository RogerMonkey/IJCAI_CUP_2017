__author__ = 'Roger'

import numpy as np

## create the csv data to analysis weather, some steps we use python to slove, and others we use mysql to create tables
shop = np.loadtxt('../data/shopid_day_num.txt', delimiter=',')

city_dict = {}
city_weather = {}
city_wind = {}
city_temp = {}
# load city weather
with open('../data/city_weather.csv') as f:
    cnt = 0
    for line in f.readlines():
        item = line.strip().split(',')
        if item[1] == '2015-12-12':
            continue
        if item[0] not in city_weather:
            city_weather[item[0]] = []
        if item[0] not in city_dict.values():
            city_dict[cnt] = item[0]
            cnt += 1
        city_weather[item[0]].append(item[4])
        # TODO: add wind and temp
        # city_wind[item[0]].append(item[5])

# simple test
print(city_weather['上海'].__len__())
print(city_dict.__len__(), city_dict)

# load city info
shop_info = {}
cat_1_dict = {}
cat_2_dict = {}
cat_3_dict = {}

# process data
with open('../data/shop_info.txt') as f:
    cnt1 = 0
    cnt2 = 0
    cnt3 = 0
    for line in f.readlines():
        item = line.strip().split(',')
        if int(item[0]) not in shop_info:
            shop_info[int(item[0])] = {}
        shop_info[int(item[0])]['city'] = item[1]
        shop_info[int(item[0])]['cat_1'] = item[7]
        shop_info[int(item[0])]['cat_2'] = item[8]
        shop_info[int(item[0])]['cat_3'] = item[9]

        if item[7] not in cat_1_dict.values():
            cat_1_dict[cnt1] = item[7]
            cnt1 += 1
        if item[8] not in cat_2_dict.values():
            cat_2_dict[cnt2] = item[8]
            cnt2 += 1
        if item[9] not in cat_3_dict.values():
            cat_3_dict[cnt3] = item[9]
            cnt3 += 1

# print(shop_info)
# print(cat_1_dict)
# print(cat_2_dict)
# print(cat_3_dict)

# if it is rain then 0 other 1
days = 488

# 0 cityid 1 cat1 2 cat2 3 cat3
cut_tag = np.zeros([2000, days + 4])

for i in range(2000):
    id = int(shop[i, 0])
    city = shop_info[id]['city']
    cat1 = shop_info[id]['cat_1']
    cat2 = shop_info[id]['cat_2']
    cat3 = shop_info[id]['cat_3']
    for j in range(488):
        wea = city_weather[city][j]

        if '雨' in wea:
            cut_tag[i, j + 4] = 1

    for cityid in city_dict:
        if city_dict[cityid] == city:
            cut_tag[i, 0] = cityid

    for catid in cat_1_dict:
        if cat_1_dict[catid] == cat1:
            cut_tag[i, 1] = catid

    for catid in cat_2_dict:
        if cat_2_dict[catid] == cat2:
            cut_tag[i, 2] = catid

    for catid in cat_3_dict:
        if cat_3_dict[catid] == cat3:
            cut_tag[i, 3] = catid

## cnt all and save csv
with open('../als/weather/weather_city.csv', 'w') as f:
    f.write('id, shop, cat_1, cat_2, cat_3, rain_cnt, nrain_cnt, rnr_cnt_rate, rain_avg, nrain_avg, rnr_avg_rate\n')
    for i in range(2000):
        id = shop[i, 0]
        city = city_dict[cut_tag[i, 0]]
        cat1 = cat_1_dict[cut_tag[i, 1]]
        cat2 = cat_2_dict[cut_tag[i, 2]]
        cat3 = cat_3_dict[cut_tag[i, 3]]

        rain = shop[i, 1:][cut_tag[i, 4:] == 1]
        no_rain = shop[i, 1:][cut_tag[i, 4:] == 0]

        rain_cnt = rain.shape[0]
        nrain_cnt = no_rain.shape[0]
        rain_avg = np.mean(rain).round(2)
        nrain_avg = np.mean(no_rain).round(2)

        r_nr_rate = (rain_avg * 1.0 / nrain_avg).round(4)
        r_nr_avg = round(rain_cnt * 1.0 / nrain_cnt, 4)
        # print(type(r_nr_rate), type(r_nr_avg))
        f.write('{0},{1},{2},{3},{4},{5},{6},{7},{8},{9}, {10}\n'.format(int(id), city, cat1, cat2, cat3, rain_cnt,
                                                                         nrain_cnt, r_nr_avg, rain_avg, nrain_avg,
                                                                         r_nr_rate))
