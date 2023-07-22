# -*- coding: utf-8 -*-
"""
Created on Thu Jun  4 20:12:35 2020

@author: User
"""

from selenium import webdriver
chromePath='C:\\Users\\User\\OneDrive\\桌面\\chromedriver.exe'
driver=webdriver.Chrome(chromePath)
url='https://shopping.pchome.com.tw/'
driver.get(url)

keyword='筆電'
driver.find_element_by_id('keyword').send_keys(keyword)
driver.find_element_by_id('doSearch').click()

from time import sleep

sleep(1)

maxprice,minprice=34000,31000
driver.find_element_by_id('MinPrice').clear()
driver.find_element_by_id('MaxPrice').clear()
driver.find_element_by_id('MinPrice').send_keys(minprice)
driver.find_element_by_id('MaxPrice').send_keys(maxprice)
driver.find_element_by_id('btn_PRC').click()

import time
scroll_pause_time=1
last_height=driver.execute_script('return document.body.scrollHeight')

while True:
    driver.execute_script('window.scrollTo(0,document.body.scrollHeight);')
    
    time.sleep(scroll_pause_time)
    
    new_height=driver.execute_script('return document.body.scrollHeight')
    if new_height == last_height:
        break
    last_height =  new_height

from bs4 import BeautifulSoup as bs
pageSource=driver.page_source
bsObj=bs(pageSource)
allGoods=bsObj.find(id='ItemContainer').findAll('dl')
goodsInfo=list()

for dl in allGoods:
    goodsName=dl.dd.next_sibling.h5.text
    goodsIntro=dl.dd.next_sibling.find('span',{'class':'nick'}).text
    goodsPrice=dl.dd.next_sibling.next_sibling.span.text
    goodsRemark=dl.dd.next_sibling.next_sibling.button.text
    
    goodsInfo.append([goodsName,goodsIntro,goodsPrice,goodsRemark])
    
    print('商品: %s\n簡介: %s\n價錢: %s\n狀態: %s\n---------------'\
          %(goodsName,goodsIntro,goodsPrice,goodsRemark))
    
import csv
with open('%s.csv'%(keyword),'w',newline='',encoding='utf-8_sig') as csvfile:
    writer=csv.writer(csvfile,delimiter=',')
    writer.writerow(['商品名稱','簡介','價錢','備註'])
    writer.writerows(goodsInfo)
        
