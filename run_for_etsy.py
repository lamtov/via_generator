#https://www.etsy.com/search/shops?ref=pagination&page=1241
import requests
from bs4 import BeautifulSoup
import os
import numpy as np
# def get_link_forums():
def create_list_link_shop():
    list_link_shop=set()
    for i in range(1,1240):
        try:
            print(i)
            req = requests.get('https://www.etsy.com/search/shops?ref=pagination&page='+str(i), verify=False)
            req.encoding = 'utf-8'
            soup = BeautifulSoup(req.text, 'lxml')
            td_has_string=soup.find_all('p', class_='wt-text-title-01 wt-text-truncate')
            #td_has_string[0]['href']

            list_shop=set()
            for td in td_has_string:
                try:
                    list_shop.add(td.text)
                except:
                    pass
            list_link_shop.update(list_shop)
        except:
            print("ERROR" + str(i))

    cur_dir = os.getcwd()
    output = open(cur_dir + '/list_shop_etsy.txt', 'w', encoding='utf-8')
    for user in list_link_shop:
        output.writelines(user + '\n')
    output.close()
def get_list_link_shop():
    result=[]
    cur_dir = os.getcwd()
    file = open(cur_dir + '/list_shop_etsy_demo.txt', 'r', encoding='utf-8')
    for line in file:
        line = line.replace('\n','')
        line="https://www.etsy.com/shop/"+str(line)+"#reviews"
        # print(line )
        result.append(line)
    return result
from test_chrome import Bot
from threading import Lock
from concurrent.futures import ThreadPoolExecutor
def do_link_shop(list_shop,i):
    # list_user_crawl = set()
    t = Bot('0.0.0.0:0', 'https://www.google.com/')
    cur_dir = os.getcwd()
    list_done=[]
    try:
        done_file = open(cur_dir + '/via_etsy_com_done_shop' + str(i) + '.txt',encoding='utf-8')
        done_list = done_file.readlines()
        for done_ in done_list:
            list_done.append(done_.replace("\n",""))
        done_file.close()
    except:
        pass

    output = open(cur_dir + '/via_etsy_com_author_' + str(i) + '.txt', 'w', encoding='utf-8')
    done_output=open(cur_dir + '/via_etsy_com_done_shop' + str(i) + '.txt','w',encoding='utf-8')
    print(cur_dir + '/via_etsy_com_author_'+str(i)+'.txt')
    for shop in list_shop:
        if shop not in list_done:
            t.set_link_spam(shop)
            list_user=t.spam_etsy_com()
            output.writelines("============ shop: "+ str(shop) + '\n')

            for user in list_user:

                output.writelines(user + '\n')
            done_output.writelines(str(shop) + '\n')
            # list_user_crawl.update(list_user)
    # print(list_user_crawl)
    done_output.close()
    output.close()

list_link_shop=get_list_link_shop()

size_lists=len(list_link_shop)
print(size_lists)
number_thread=2
for i in range(0,number_thread):
    try:
        list_shop=list_link_shop[i*int(size_lists/number_thread):(i+1)*int(size_lists/number_thread)]
        executor = ThreadPoolExecutor(1)
        executor.submit(do_link_shop,list_shop,i)
    except Exception as e:
        print(e)
