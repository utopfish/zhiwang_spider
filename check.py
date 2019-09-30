# -*- coding=utf-8 -*-
#@author:liuAmon
#@contact:utopfish@163.com
#@file:check.py
#@time: 2019/9/3 23:54
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from exceptions_spider import NOTUSABLEEXCEPTION
from selenium.common.exceptions import TimeoutException
from selenium import webdriver

def check_visible(driver:webdriver, target:tuple, timeout=10):
    """
        检查元素是否可见
    """
    wait = WebDriverWait(driver, timeout)
    try:
        element = wait.until(EC.visibility_of_element_located(target))
    except TimeoutException:
        raise NOTUSABLEEXCEPTION('元素超时不可访问')
    else:
        return element