# -*- coding=utf-8 -*-
#@author:liuAmon
#@contact:utopfish@163.com
#@file:spider_main.py
#@time: 2019/9/4 0:45
import os
import time
import json
from check import *
from config import cf
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

class zhiwang_spider():
    def __init__(self):
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        self.paperSavePath=cf['paperPath']
        self.recordSavePath=cf['record']
        prefs = {
            'profile.default_content_setting_values':
                {
                    'notifications': 2
                },
            'download.default_directory': self.paperSavePath
        }
        options.add_experimental_option('prefs', prefs)
        driver = webdriver.Chrome(chrome_options=options)
        self.driver=driver

    def set_type_keyword(self, type, kw):
        '''
        输入搜索类型与关键字
        :param type: (str)论文类型(期刊或会议)
        :param kw: (str)关键字
        :return:
        '''
        self.driver.get('http://kns.cnki.net/kns/brief/default_result.aspx')
        time.sleep(5)
        if type == "期刊论文":
            self.driver.find_element_by_id("CJFQ").click()
        elif type == "会议论文":
            self.driver.find_element_by_id("CIPD").click()
        self.driver.find_element_by_name('txt_1_value1').send_keys(kw)
        self.driver.find_element_by_xpath('//select[@id="txt_1_sel"]').click()
        self.driver.find_element_by_id('btnSearch').click()
        time.sleep(5)
    def switch_page(self,year):
        '''
        页面切换到内获取内容的部分
        :param year:
        :return:
        '''
        self.driver.get(
            'http://kns.cnki.net/kns/brief/brief.aspx?ctl=4a7fde68-1a44-4852-8b23-1a70aeb4cf8b&dest=%E5%88%86%E7%BB%84%EF%BC%9A%E5%8F%91%E8%A1%A8%E5%B9%B4%E5%BA%A6%20%E6%98%AF%20{}&action=5&dbPrefix=SCDB&PageName=ASP.brief_default_result_aspx&Param=%e5%b9%b4+%3d+%27{}%27&SortType=(FFD%2c%27RANK%27)+desc&ShowHistory=1&isinEn=1'.format(year,year))
    def click_page(self,page):
        '''
        点击到需要的页面
        :param page:
        :return:
        '''
        for i in range(page):
            a_list = self.driver.find_elements_by_xpath('//div[@class="TitleLeftCell"]//a')
            for a in a_list:
                if (a.text == '下一页'):
                    a.click()
                    break
    def next_page(self):
        '''
        点击正确返回True，无下一页返回Flase
        :return:
        '''
        a_list = self.driver.find_elements_by_xpath('//div[@class="TitleLeftCell"]//a')
        for a in a_list:
            if (a.text == '下一页'):
                a.click()
                time.sleep(4)
                return True
        return False
    def get_list(self,log,number,classification):
        '''
        论文内容下载
        :param num:
        :param classification:
        :return:
        '''
        elements = self.driver.find_elements_by_xpath('//table[@class="GridTableContent"]//tr[@bgcolor]')
        time.sleep(5)
        for index,element in enumerate(elements):
            if index<log[number]['row']:
                continue
            try:
                log[number]['row']=log[number]['row']+1
                data={}
                data['title']=""
                data['anther_title']=""
                data['author']=""
                data['keyword']=""
                data['abstract']=""
                data['anther_abstract']=""
                data['project_belong']=""
                data['originization']=""
                data['journal']=""
                data['publish_date']=""
                data['publish_year']=""
                data['volume']=""
                data['issue']=""
                data['official_url']=""
                data['pagemark']=""
                data['total_page']=""
                data['bagin_page']=""
                data['end_page']=""
                data['ref']=""
                data['download_url']=""
                data['collected_info']=""
                data['meeting_info']=""
                data['basic_classification']=""
                data['issn']=""
                data['cn']=""
                data['language']=""
                data['type']=""
                data['attach']=""
                info=element.find_elements_by_css_selector("td")
                data['title']=info[1].text
                data['author']=info[2].text
                data['journal']=info[3].text
                data['publish_date']=info[4].text
                data['publish_year']=info[4].text.split("-")[0]
                data['type']=info[5].text
                a = element.find_element_by_xpath('td/a[@class="fz14"]')
                a.click()


                windows = self.driver.window_handles
                self.driver.switch_to.window(windows[-1])
                time.sleep(5)
                data['download_url'] = self.driver.current_url
                if is_Chinese(data['title']):
                    data['language']="中文"
                else:
                    data['language']="english"

                print("================================开始================")
                try:
                    origaniztion=self.driver.find_element_by_css_selector(".orgn > span:nth-child(1) > a:nth-child(1)").text
                    print("单位"+origaniztion)
                    data['originization']=origaniztion
                except:
                    pass
                try:
                    abstract=self.driver.find_element_by_css_selector("span#ChDivSummary").text
                    print("摘要"+abstract)
                    data['abstract']=abstract
                except:
                    pass
                try:
                    for i in self.driver.find_elements_by_css_selector(".wxBaseinfo > p"):
                        if i.find_element_by_css_selector("label").text=="关键词：":
                            keyword=i.text
                            print("关键字"+keyword[4:])
                            data['keyword']=keyword[4:]
                        if i.find_element_by_css_selector("label").text=="基金：":
                            belong_project=i.text
                            print("所属项目:"+belong_project[3:])
                            data['project_belong']=belong_project[3:]
                except:
                    pass
                try:
                    for i in self.driver.find_elements_by_css_selector("div.info >div.total > span"):
                        if i.find_element_by_css_selector("label").text=="页码：":
                            pagemark=i.find_element_by_css_selector("b").text
                            print("页码"+pagemark)
                            data['pagemark']=pagemark
                            data['bagin_page']=pagemark.split("-")[0]
                            data['end_page']=pagemark.split("-")[1]
                        if i.find_element_by_css_selector("label").text=="页数：":
                            pagenumber=i.find_element_by_css_selector("b").text
                            print("页数"+pagenumber)
                            data['total_page']=pagenumber

                except Exception as e:
                    print(e)
                try:
                    issue=self.driver.find_element_by_css_selector(".sourinfo > p:nth-child(3) > a:nth-child(1)").text
                    print("期号"+issue)
                    data['issue']=issue
                except:
                    pass
                try:
                    issn=self.driver.find_element_by_css_selector(".sourinfo > p:nth-child(4)").text
                    print("issn"+issn)
                    data['issn']=issn
                    data['basic_classification']=classification
                except:
                    pass
                print("=======================结束===================================")
                try:
                    sub_btn = check_visible(self.driver, (By.ID, "pdfDown"), 10)
                    if ";" in data['author']:
                        name = data['author'].split(";")[0]
                    else:
                        name = data['author']
                    data['attach'] = data['title'] + "_"+name + ".pdf"
                except NOTUSABLEEXCEPTION as e:
                    e.msg = 'pdf下载失败'
                    raise e
                ActionChains(self.driver).move_to_element(sub_btn).click(sub_btn).perform()
            except Exception as arg:
                print(arg)

            try:

                with open(os.path.join(self.recordSavePath, "record.json"), "a+") as f:
                    json.dump(data, f)
                    f.write('\n')
                    print("加载入文件完成...")
            except:
                print("文件加载错误")
            try:
                with open(os.path.join("log.json"), "w") as f:
                    json.dump(log, f)
                    f.write('\n')
                    print("日志文件row更新")
            except:
                print("日志文件row更新错误")
            self.driver.close()
            self.driver.switch_to_window(windows[0])
            time.sleep(5)
        # return log
    def close(self):
        self.driver.quit()

def is_Chinese(word):
    '''
    判断是否为中文，
    :param word: 输入标题
    :return: True 中文，False英文
    '''
    for ch in word:
        if '\u4e00' <= ch <= '\u9fff':
            return True
    return False


def takeYear(elem):
    return elem['year']

def init_record():
    li=[]
    d=cf["clssifiction"]
    for i in d:
        for cate,keywords in i.items():
            for keyword in keywords:
                for year in range(2000,2019):
                    data = {}
                    data["cate"]=cate
                    data["keyword"]=keyword
                    data["year"]=year
                    data['nowPage']=0
                    data['row']=0
                    data['stop']=False
                    li.append(data)
    li.sort(key=takeYear,reverse=True)
    with open(os.path.join("log.json"), "a") as f:
        json.dump(li, f)
        f.write('\n')
        print("加载入文件完成...")
if __name__ == "__main__":
    '''
    todo List:
    1.解决爬取一定时间，页面不能访问问题
    2.加入分布想法，让程序在不同机器上，爬取不同数据（先不考虑分布式，修改driver.get中链接的参数能解决一部分问题）
    3.加入异常结束重来的问题，将运行参数存储起来，程序异常结束后重新开始，先去到异常出现位置
    4.数据清理问题，对最后保存的结果，对缺失较大的样本删除数据。
    5.对下载路径中保存的文件进行检测，数据库中没有的文件进行删除，数据库有文件路径中没有的进行报错提示。
    6.加入英文论文搜索模板
    7.加入对参考文献的爬取
    8.对样本的要求的其他内容尽量爬取
    
'''

    part=10#将全部内容分为10份
    no=0#第一份
    log=[]
    if os.path.exists("log.json") != True:
        init_record()
    with open('log.json', encoding='utf-8') as f:
            line = f.readline()
            d=json.loads(line)
            for i in d:
                log.append(i)
    for i in range(int(len(log)/part)):
            number=no*int(len(log)/part)+i
            print(log[number])
            while log[number]['stop']==False:
                robot = zhiwang_spider()
                robot.set_type_keyword("期刊论文", log[number]["keyword"])
                robot.switch_page(log[number]['year'])
                robot.click_page(log[number]['nowPage'])
                try:
                    check_visible(robot.driver, (By.CLASS_NAME, "GridTableContent"), 10)
                except:
                    robot.close()
                    continue
                robot.get_list(log,number,log[number]["cate"])
                sign=robot.next_page()
                t=log[number]
                log[number]['nowPage']=log[number]['nowPage']+1
                log[number]['row']=0
                with open(os.path.join("log.json"), "w") as f:
                    json.dump(log, f)
                    f.write('\n')
                    print("日志文件更新")
                robot.close()
                if sign==False:
                    log[number]['stop']=True

