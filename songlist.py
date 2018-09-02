#coding=utf-8
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import csv

url = 'https://music.163.com/#/discover/playlist/?order=hot&cat=%E5%85%A8%E9%83%A8&limit=35&offset=0'

#driver = webdriver.PhantomJS()
#todo: 配置chrome driver的入参 == headless：？ disable-gpu：？
chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')
driver = webdriver.Chrome(chrome_options=chrome_options)
#todo: 这一步的driver大概支持哪些方法？

csv_file = open('playlist.csv','w', newline='')
writer = csv.writer(csv_file)
writer.writerow(['标题','播放数','链接'])

#解析每一页，直到“下一页”为空 -- 下一页为空的时候，他的href="javascript:void(0)"
while url != 'javascript:void(0)':
    driver.get(url)
    #todo: 用webdriver加载页面 -- 为什么是get？支持多少种加载页面的方法？有多少不同？
    driver.switch_to.frame("contentFrame")
    #切换到内容的iframe，什么是iframe？frameVSiframe, iframe是一种内嵌在网页中的框架
    data = driver.find_element_by_id('m-pl-container').find_elements_by_tag_name('li')
    #哪里使用element，什么情况下使用elements？定位歌单标签 -- 'm-pl-container' -- 可以用class来定位歌单嘛？
    #class是用于指定element使用哪种css的样式的类，不属于html用于表达结构的标签

    for dataelement in data:
        #解析当前页面中的歌单
        nb = dataelement.find_element_by_class_name('nb').text
        #获取播放数
        if '万' in nb and int(nb.split('万')[0])>500:
            #为什么要》500才做以下操作？
            msk = dataelement.find_element_by_css_selector('a.msk')
            #css_selector有哪些可能的入参可以选?是a.classname嘛？并且当作一个对象，可以操作他的里面的内容？
            #<a href="xxxxx" class="zbtn znxt">下一页</a>
            writer.writerow([msk.get_attribute('title'), nb, msk.get_attribute('href')])
            #然后将msk对象中的title和href写入csv

    url = driver.find_element_by_css_selector('a.zbtn.znxt').get_attribute('href')
    #把下一页的url存为url

csv_file.close()