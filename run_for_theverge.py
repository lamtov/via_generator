import requests
from bs4 import BeautifulSoup
import os
import numpy as np
def get_link_forums():

    req = requests.get('https://www.theverge.com/forums', verify=False)
    req.encoding = 'utf-8'
    soup = BeautifulSoup(req.text, 'lxml')
    td_has_string=soup.find_all('a', class_='forum-icon-link')
    #td_has_string[0]['href']

    list_link_forums=[td['href'] for td in td_has_string]
    # td_has_string[0].contents[0].contents[0].text.replace(" ", "")

    # list_name=[td.contents[0].contents[0].text.replace(" ", "") for td in td_has_string]
    # list_name
    return list_link_forums
def find_tr(tag):
    return tag.name=='tr' and (len(tag.contents)>0 and  tag.contents[0].name=='td' or tag.contents[1].name=='td'   )
def find_list_post(link):
    def find_tr(tag):
        return tag.name=='tr' and (len(tag.contents)>0 and  tag.contents[0].name=='td' or tag.contents[1].name=='td'   )

    req = requests.get(link, verify=False)
    req.encoding = 'utf-8'
    soup = BeautifulSoup(req.text, 'lxml')
    tr_has_string=soup.find_all(find_tr)

    list_posts=[]
    for tr in tr_has_string:
        for td in  tr.contents:
            if td.name=='td' and  len(td.contents)>0 and  (td.contents[0].name=='a' or td.contents[1].name=='a' ) :
                if td.contents[0].name=='a' :
                    list_posts.append(td.contents[0]['href'])
                else :
                    list_posts.append(td.contents[1]['href'])
                break
    return list_posts

def find_list_author(link):
    def find_tr(tag):
        return tag.name == 'tr' and (
                    len(tag.contents) > 0 and tag.contents[0].name == 'td' or tag.contents[1].name == 'td')

    req = requests.get(link, verify=False)
    req.encoding = 'utf-8'
    soup = BeautifulSoup(req.text, 'lxml')
    tr_has_string = soup.find_all(find_tr)

    list_authors = set()
    for tr in tr_has_string:
        if len(tr.contents) > 1:
            try:
                for td in tr.contents[2:]:
                    if td.name == 'td' and len(td.contents) > 0 and (
                            td.contents[0].name == 'a' or td.contents[1].name == 'a'):
                        if td.contents[0].name == 'a':
                            list_authors.add(td.contents[0].text)
                        else:
                            list_authors.add(td.contents[1].text)
                        break
            except:
                print(link)
    return list_authors

def get_list_link_post_forums(link_forum):
    def find_tr(tag):
        return tag.name == 'tr' and (
                    len(tag.contents) > 0 and tag.contents[0].name == 'td' and tag.contents[0].contents[0].name == 'a')


    num_post = 1
    page = 1
    list_link_post_forums = []
    list_authors=set()
    while num_post != 0:
        link = link_forum + '/' + str(page)

        list_post = find_list_post(link)
        _list_author = find_list_author(link)

        num_post = len(list_post)
        page = page + 1
        list_link_post_forums = list_link_post_forums + list_post
        list_authors.update(_list_author)
    return list_link_post_forums, list_authors

if __name__ == "__main__":
    from test_chrome import Bot

    t = Bot('0.0.0.0:0', 'https://www.google.com/')

    list_user_crawl=set()
    list_link_forums=get_link_forums()
    for link_forum in list_link_forums:
        list_link_post_forums,list_authors = get_list_link_post_forums(link_forum)
        list_user_crawl.update(list_authors)

    #     for link_post in list_link_post_forums:
    #         t.set_link_spam(link_post)
    #         # t.spam()
    #         list_users,author=t.spam_theverge_com()
    #         list_user_crawl.update(list_users)
    #         list_user_crawl.add(author)
    #
    # # print(list_user_crawl)
    cur_dir = os.getcwd()
    output = open(cur_dir + '/via_theverge_author.txt', 'w', encoding='utf-8')
    for user in list_user_crawl:
        output.writelines(user + '\n')
    output.close()
