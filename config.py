#!/usr/bin/env python
# -*- coding:UTF-8 -*-
'''
@author: HG
@contact: 18165271995@163.com
@file: config.py
@time: 2019/9/30 15:41
'''
#配置论文，记录保存路径
from easydict import EasyDict
cf=EasyDict()
cf.paperPath="D:\paper07"
cf.record=r"D:\record07"
# cf.clssifiction=[{"载人航天":["载人 航天","载人 登月","载人 飞船"]},{"深空探测":["深空 探测","月球 探测","火星 探测","小行星 探测","月球 探测器","月球 着陆器","火星车","火星 探测器","火星 着陆器","小行星 探测器","脉冲星"]}]
cf.clssifiction=[{"载人航天":["空间站","国际空间站","航天飞机","探索飞行器","货运飞船","光学舱","空间实验室"]},{"深空探测":["嫦娥一号","嫦娥二号","嫦娥三号","嫦娥四号","嫦娥五号","天体探测","巡视探测","探月计划","探月工程"]}]
