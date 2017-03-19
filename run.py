# -*- coding: utf-8 -*-
import sys
from main.data_processing import run as dp_run
from main.model import run as model_run
from main.rule import run as rule_run
from main.fuse import run as fuse_run

def run():
    '''
    数据预处理
    :return:
    '''
    dp_run()

    '''
    跑模型
    '''
    model_run()

    '''
    模型融合
    '''
    fuse_run()

    '''
    跑规则
    '''
    rule_run()
