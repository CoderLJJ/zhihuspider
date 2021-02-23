import os
import re
import requests
import pandas as pd
import xlrd
from selenium.common.exceptions import NoSuchElementException
from selenium import webdriver
Domain_Name = 'https:'

def hot():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
        'Referer': "https://www.zhihu.com/billboard"
    }
    url = 'https://www.zhihu.com/billboard'
    response = requests.get(url, headers=headers)
    html = response.text
    print('----------------开始爬取----------------')
    title = re.findall(r'<div class="HotList-itemTitle">([\s\S]+?)</div>', html, re.M)  # 获取问题内容
    hot = re.findall(r'<div class="HotList-itemMetrics">([\s\S]+?)</div>', html, re.M)  # 获取问题热度
    url = re.findall(r'"link":{"url":"([\s\S]+?)"}},', html, re.M)  # 获取问题超链接
    dts = []
    for i in range(len(title)):
        lst = []
        lst.append(title[i])
        lst.append(hot[i])
        lst.append(str(url[i]).replace('u002F', '').replace('\\', '/'))
        dts.append(lst)
    df = pd.DataFrame(dts, columns=['title', 'hot', 'links'])
    df.to_excel('./zhihu-billboard' + '.xlsx', encoding='gbk')
    print('知乎热榜文章网址爬取完成,开始爬取网址内容')
def Zhihu():
    options = webdriver.ChromeOptions()
    options.add_argument('--user-data-dir=C:/Users/81316/AppData/Local/Google/Chrome/User Data/Default') # 个人资料路径必须是斜杆 /，不能是反斜杆 \
    browser = webdriver.Chrome(options=options)
    data = xlrd.open_workbook('zhihu-billboard.xlsx')
    table = data.sheets()[0]
    links = table.col_values(int(3))
    dfData = []
    b = 0
    n = 0
    if not os.path.exists("admin"):
        os.mkdir("admin")
    if not os.path.exists("user"):
        os.mkdir("user")
    for url in links[1:]:
        b += 1
        n += 1
        browser.get(url)
        try:
            title = browser.find_element_by_xpath('//div[@class="QuestionHeader"]/div[@class="QuestionHeader-content"]/div[@class="QuestionHeader-main"]/h1[@class="QuestionHeader-title"]').text
            answernum = browser.find_element_by_xpath('//div[@class="List-header"]/h4[@class="List-headerText"]').text
            followers = browser.find_element_by_xpath('//button/div[@class="NumberBoard-itemInner"]/strong[@class="NumberBoard-itemValue"]').text
            browse = browser.find_element_by_xpath('//div[@class="NumberBoard-item"]/div[@class="NumberBoard-itemInner"]/strong').text
            browser.find_element_by_xpath('//div[@class="QuestionHeaderActions"]/div[@class="Popover"]/button[@type="button"]').click()
            browser.find_element_by_xpath("//div[@class='Menu QuestionHeader-menu']/a").click()
            time =browser.find_element_by_xpath('//*[@id="zh-question-log-list-wrap"]/div[@class="zm-item"][1]/div[3]/time').text
            dfData.append({'标题': title, '回答数': answernum, '关注数': followers, '被浏览数': browse, '网址': url, '热榜时间': time})
            first = browser.find_element_by_xpath('//*[@id="zh-question-log-list-wrap"]/div[@class="zm-item"][1]')
            first.screenshot(f'admin\\{b}.png'.format(b=b))
            sum = browser.find_elements_by_xpath('//*[@id="zh-question-log-list-wrap"]/div[@class="zm-item"]')
            xpath_rule = "//*[@id='zh-question-log-list-wrap']/div[@class='zm-item']" + str([len(sum)])
            second = browser.find_element_by_xpath(xpath_rule)
            browser.execute_script('arguments[0].scrollIntoView();', second)
            second.screenshot(f'user\\{n}.png'.format(n=n))
        except NoSuchElementException:
            print("No Such Element")
    keys = dfData[0].keys()
    pd.DataFrame(dfData, columns=keys).to_csv('data.csv', encoding='utf-8-sig')
    browser.quit()

if __name__ == '__main__':
    hot()
    Zhihu()