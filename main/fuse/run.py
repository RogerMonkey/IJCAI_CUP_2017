# -*- coding: utf-8 -*-
from fuse import model_fuse
import time

def run_fuse():
    version = time.strftime('%Y-%m-%d', time.localtime(time.time())) + '_'
    filename1='../../data/results/result_2017-03-16_special_day_weather_huopot.csv'
    filename2='../../data/results/result_2017-03-11_special_day_weather_huopot.csv'
    filename3 = '../../data/results/result_' + version + 'fuse.csv'
    model_fuse(filename1,filename2,filename3)

if __name__ == '__main__':
    run_fuse()