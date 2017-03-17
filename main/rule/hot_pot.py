# -*- coding: utf-8 -*-
import numpy as np

'''
这里对火锅店进行处理，对于第二周上浮一定比例
统计了部分2015年11月1-7 相对于 11月8-14 的比例，发现整体提高了一些
'''


def hot_pot():
    filename = "../../data/statistics/shop_info.txt"
    fr = open(filename)
    is_hot = {}
    for line in fr.readlines():
        data = line.strip().split(",")
        if data[-2] == "火锅":
            is_hot[int(data[0])] = 1
    return is_hot


def base_hot_pot(filename, fileto, is_hot):
    predict = np.loadtxt(filename, delimiter=',')
    for i in range(predict.shape[0]):
        # print len(predict[i,1:])
        for j in range(1, len(predict[i])):
            if j > 7 and is_hot.get(predict[i, 0], 0) == 1:
                predict[i, j] = predict[i, j] * 1.025 + 0.5
    np.savetxt(fileto, predict, fmt='%d', delimiter=',')

if __name__ == '__main__':
    pass