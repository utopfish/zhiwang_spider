# -*- coding=utf-8 -*-
#@author:liuAmon
#@contact:utopfish@163.com
#@file:watch.py
#@time: 2019/10/16 19:15
import os
import time
import subprocess
from config import cf

def restart_process(process_name):
    red = subprocess.Popen('tasklist', stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    tasklist_str = red.stdout.read().decode(encoding='gbk')
    re_path = process_name.split("\\")[-1]
    if tasklist_str.index(re_path)==tasklist_str.rindex(re_path):

        os.system("{}/Scripts/activate.bat && python {}/spider_main.py".format(cf['venv'],cf['rootdir']))

    else:
        print( '第' + str(count) + '次检测正在运行中')
        print("程序正常运行")
        pass
        # global error_count
        # error_count += 1

global count
count=0
while True:
    time.sleep(300)
    count+=1
    restart_process("python.exe")
