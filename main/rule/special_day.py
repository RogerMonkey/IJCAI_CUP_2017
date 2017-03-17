# -*- coding: utf-8 -*-
import numpy as np

'''
某些特殊天的规则
对11月11号的数据进行一定幅度的调整
（具体参数通过2015年统计得到）
统计发现对于大城市，11的提高反而会少一些
对于23和1556两个商家存在太多的异常天，我们人工进行了修正
'''

def getShop_City():
    filename="../../data/statistics/shop_info.txt"
    shop_city = {}
    fr = open(filename)
    for line in fr.readlines():
        data = line.strip().split(",")
        shop_city[int(data[0])] = data[1]
    return shop_city


def big_city(filename, fileto, shop_city):
    list_23 = [23, 102, 106, 104, 110, 94, 91, 115, 102, 106, 104, 117, 95, 91, 112]
    list_1556 = [1556, 208, 192, 201, 196, 170, 179, 213, 208, 192, 201, 216, 178, 179, 206]
    citys = ["上海", "杭州", "北京", "广州", "南京", "武汉", "深圳"]  #
    predict = np.loadtxt(filename, delimiter=',')
    for i in range(predict.shape[0]):
        shop_id = predict[i, 0]
        for j in range(1, len(predict[i])):
            if predict[i, 0] == 1824:
                predict[i, j] = 51
            if predict[i, 0] == 23:
                predict[i, j] = list_23[j]
            if predict[i, 0] == 1556:
                predict[i, j] = list_1556[j]
            if j == 11:
                if shop_city[shop_id] in citys:
                    predict[i, j] = predict[i, j] * 1.03 + 0.5  # 1.03
                else:
                    predict[i, j] = predict[i, j] * 1.09 + 0.5  # 1.09
            if j == 12:
                predict[i, j] = predict[i, j] * 1.025 + 0.5  # 1.025
            if j == 14:
                predict[i, j] = predict[i, j] * 0.96 + 0.5
    np.savetxt(fileto, predict, fmt='%d', delimiter=',')


if __name__ == '__main__':
    pass

