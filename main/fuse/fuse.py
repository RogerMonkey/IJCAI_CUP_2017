# -*- coding: utf-8 -*-
import numpy as np

'''
模型融合

这里直接对多个模型进行了加权融合
1.对模型得到的结果进行融合
2.对模型加规则后的结果进行融合
3.模型主要是ExtraTree中特征选择，时间序列模型，RandomForestRegressor以及GBDT
'''

def model_fuse(filename1, filename2, fileto, x=0.6):
    a = np.loadtxt(filename1, delimiter=',')
    b = np.loadtxt(filename2, delimiter=',')
    a[:, 1:] = (a[:, 1:] * x + b[:, 1:] * (1 - x) + 0.5).round()
    np.savetxt(fileto, a, delimiter=',', fmt='%d')


if __name__ == '__main__':
    pass
