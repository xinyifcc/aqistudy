#-*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import requests
#city encode
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

base_url = 'https://www.aqistudy.cn/historydata/daydata.php?city='
str_city = '北京'

def get_month_set():
    global month_set, i
    month_set_i = [i for i in range(1, 13)]
    month_set = list()
    for i in range(7, 10):
        month_set.append(('2015-0%s' % i))
    for i in range(10, 13):
        month_set.append(('2015-%s' % i))
    for i in range(1, 10):
        month_set.append(('2016-0%s' % i))
    month_set.append(('2016-%s' % 10))
    month_set.append(('2016-%s' % 11))
    return month_set

def get_city_set():
    str_file = r'city.txt'
    fp = open(str_file,'rb')
    city_set = list()
    for line in fp.readlines():
        city_set.append(str(line.strip()))
    return city_set

month_set = get_month_set()
city_set = get_city_set()

city_dic = dict()
for city in city_set:
    file_name = city + '.csv'
    fp = open('aqi/' + file_name, 'w')
    for i in range(len(month_set)):
        str_month = month_set[i]
        weburl = ('%s%s&month=%s' % (base_url,city,str_month))
        response = requests.get(weburl).content
        soup = BeautifulSoup(response,'html.parser',from_encoding='utf-8')
        result = soup.find_all('td',attrs={'align':'center'},recursive=True)

        for i in range(0,len(result) - 11,11):
            tag_date = result[i]
            tag_aqi = result[i + 1]
            record_day = tag_date.get_text().strip()
            record_aqi = tag_aqi.get_text().strip()
            fp.write(('{0},{1},{2}\n'.format(record_day,record_aqi,city))) #在这边加了city以便后期合并文本
        print('{0}---{1},{2}---DONE'.format(city_set.index(city), city, str_month))
    fp.close()
