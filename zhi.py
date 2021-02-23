import os
import xlrd
from selenium.common.exceptions import NoSuchElementException
from selenium import webdriver
import pandas as pd
def ZhihuSpider(filename):
    options = webdriver.ChromeOptions()
    options.add_argument('--user-data-dir=C:/Users/81316/AppData/Local/Google/Chrome/User Data/Default') # 个人资料路径必须是斜杆 /，不能是反斜杆 \
    browser = webdriver.Chrome(options=options)
    data = xlrd.open_workbook(filename)
    table = data.sheets()[0]
    try:
        a = input("#0 1 2 3分别对应第一，二，三，四列，依次递增......请输入你要爬取的网址所在列:")
    except:
        print("请正确输入你要爬的网址所在列")
    links = table.col_values(int(a))
    dfData = []
    a = 0
    b = 0
    if not os.path.exists("first"):
        os.mkdir("first")
    if not os.path.exists("second"):
        os.mkdir("second")
    for url in links[1:]:
        a += 1
        b +=1
        browser.get(url)
        try:
            title = browser.find_element_by_xpath('//div[@class="QuestionHeader"]/div[@class="QuestionHeader-content"]/div[@class="QuestionHeader-main"]/h1[@class="QuestionHeader-title"]').text
            answernum = browser.find_element_by_xpath('//div[@class="List-header"]/h4[@class="List-headerText"]').text
            followers = browser.find_element_by_xpath('//button/div[@class="NumberBoard-itemInner"]/strong[@class="NumberBoard-itemValue"]').text
            browse = browser.find_element_by_xpath('//div[@class="NumberBoard-item"]/div[@class="NumberBoard-itemInner"]/strong').text
            browser.find_element_by_xpath('//div[@class="QuestionHeaderActions"]/div[@class="Popover"]/button[@type="button"]').click()
            browser.find_element_by_xpath("//div[@class='Menu QuestionHeader-menu']/a").click()
            time = browser.find_element_by_xpath('//*[@id="zh-question-log-list-wrap"]/div[@class="zm-item"][1]/div[3]/time').text
            dfData.append({'标题': title, '回答数': answernum, '关注数': followers, '被浏览数': browse, '网址': url, '热榜时间': time})
            first = browser.find_element_by_xpath('//*[@id="zh-question-log-list-wrap"]/div[@class="zm-item"][1]')  # 知乎管理员锁定编辑
            first.screenshot(f'first\\{a}.png'.format(a=a))
            sum = browser.find_elements_by_xpath('//*[@id="zh-question-log-list-wrap"]/div[@class="zm-item"]') #某人添加了问题
            xpath_rule = "//*[@id='zh-question-log-list-wrap']/div[@class='zm-item']" + str([len(sum)])
            second = browser.find_element_by_xpath(xpath_rule)
            browser.execute_script('arguments[0].scrollIntoView();', second)
            second.screenshot(f'second\\{b}.png'.format(b=b))
        except NoSuchElementException:
            print("No Such Element")
    keys = dfData[0].keys()
    pd.DataFrame(dfData, columns=keys).to_csv('zhihudata.csv', encoding='utf-8-sig')
    browser.quit()
