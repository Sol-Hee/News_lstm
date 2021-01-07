from selenium import webdriver
import time
import urllib.request as req
from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys
from urllib.parse import quote
from urllib.request import urlopen
import pandas as pd

driver = webdriver.Chrome("path to chromedriver")
url = "http://joongang.joins.com"
driver.get(url)

driver.find_element_by_class_name('icon_search').click()
input=driver.find_element_by_id("searchKeyword")
input.send_keys('코로나')
driver.find_element_by_id("btnSearch").click()
driver.find_element_by_class_name("view_more").click()
driver.find_element_by_class_name("view_more").click()

link = []
for i in range(1, 41):
    print('{}번째 page.....'.format(i))
    time.sleep(15)
    # get html
    html = driver.page_source
    soup = BeautifulSoup(html,"html.parser")
    soup = soup.select("ul.list_default > li")

    # get url
    for j in soup:
        href = j.find('a', {'target': '_blank'})['href']
        link.append(href)

    if i < 10:
        # 1 page -> 2 page
        if i == 1:
            driver.find_element_by_xpath('//*[@id="content"]/div[3]/div[3]/div/a[1]').click()
            continue
        # n -> n+1 page (2<= n <= 9)
        else:
            driver.find_element_by_xpath('//*[@id="content"]/div[2]/div[3]/div/a[{}]'.format(i)).click()
            continue
    if i == 10:
        driver.find_element_by_class_name("btn_next").click()
        continue

    if i > 10:
        driver.find_element_by_xpath('//*[@id="content"]/div[2]/div[3]/div/a[{}]'.format(i%10+1)).click()
        continue

    if i % 10 == 0 :
        driver.find_element_by_class_name("btn_next").click()


link=set(link)
link=list(link)

links=pd.Series(link)
links.to_csv("../news_link.csv",index=False)

url= link[0]
html = urlopen(url)
soup=BeautifulSoup(html, 'html.parser')
soup.select_one('div.article_body').get_text()


with open("/Users/solhee/data/news_joongang.txt","a") as file:
    for i,v in enumerate(link):
        print('{}번째 실행중 ...........'.format(i+1))
        print('url :', v)
        url = v
        html = urlopen(url)
        soup = BeautifulSoup(html, 'html.parser')
        text = soup.select_one('div.article_body').get_text()
        print(text)
        file.write(text)
        time.sleep(30)
