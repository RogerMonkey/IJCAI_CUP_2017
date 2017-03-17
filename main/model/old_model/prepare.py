__author__ = 'roger'

import numpy as np
import datetime

## prepare data
base_path = "../../../data/statistics/"


def load_data_as_npdict():
    shop = {}
    index = {}
    begin_time = datetime.date(2015, 7, 1)
    with open(base_path + 'shopid_day_num.txt', 'r') as f:
        for line in f.readlines():
            item = line.strip().split(',')
            shopId = int(item[0])
            if shopId not in shop:
                shop[shopId] = np.array(item[1:], 'f')

    for i in range(489):
        if begin_time + datetime.timedelta(i) != datetime.date(2015, 12, 12):
            index[i] = begin_time + datetime.timedelta(i)
    return index, shop


def change_date_to_str(date):
    return '-'.join([str(date.year), str(date.month), str(date.day)])


if __name__ == '__main__':
    index, shop = load_data_as_npdict()
    for i in shop:
        print(shop[i])
