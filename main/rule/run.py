# -*- coding: utf-8 -*-
from weather import *
from hot_pot import *
from special_day import *
import time

def all_rule():
    version = time.strftime('%Y-%m-%d', time.localtime(time.time())) + '_'
    filename1='../../data/results/result_' + version + '.csv'
    filename2='../../data/results/result_' + version + 'special_day.csv'
    filename3 = '../../data/results/result_' + version + 'special_day_weather.csv'
    filename4 = '../../data/results/result_' + version + 'special_day_weather_huopot.csv'
    shop_city = getShop_City()
    big_city(filename1, filename2, shop_city)

    weather_rule(filename2, filename3)

    is_hot = hot_pot()
    base_hot_pot(filename3, filename4, is_hot)

if __name__ == '__main__':
    all_rule()