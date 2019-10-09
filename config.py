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
cf.paperPath="D:\paper"
cf.record=r"D:\record"

cf.clssifiction=[{"载人航天":["载人 航天","载人 登月","载人 飞船"]},{"深空探测":["深空 探测","月球 探测","火星 探测","小行星 探测","月球 探测器","月球 着陆器","火星车","火星 探测器","火星 着陆器","小行星 探测器","脉冲星"]}]
