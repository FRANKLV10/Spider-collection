from selenium import webdriver
import os
import time
import re
from  bs4 import BeautifulSoup
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.wait import WebDriverWait
import win32api
import win32con
import selenium
import requests
def url(html):
    #获取首页每个帖子地址
    data = []
    r = requests.get('%s'%html)
    r = r.text
    text = r
    soup = BeautifulSoup(text,'lxml')
    for tag in  soup.find_all('div',class_="threadlist_title pull_left j_th_tit "):

        a = tag.find('a')
        herf = re.findall(r'href="(.*)" target=',str(a))

        data.append(herf[0])
    del data[0]
    return data


def login(data,username,password,text,html):
    abspath = os.path.abspath(r"C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe")
    dr = webdriver.Chrome(abspath)

    dr.get("%s"%html)
    dr.find_element_by_id('com_userbar').click()
    time.sleep(5)


    #登录功能
    username_input = dr.find_element_by_id('TANGRAM__PSP_11__userName')
    password_input = dr.find_element_by_id('TANGRAM__PSP_11__password')
    login = dr.find_element_by_id('TANGRAM__PSP_11__submit')
    username_input.clear()
    username_input.send_keys(username)  # 填写用户名
    time.sleep(0.2)
    password_input.clear()
    password_input.send_keys(password)  # 填写密码
    time.sleep(0.2)

    login.click()

    time.sleep(5)
    #回复首页每一个帖子
    for i in data:
        try:
            dr.get('http://tieba.baidu.com/%s'%i)
            time.sleep(5)
            time.sleep(2)
            js = "document.getElementById('ueditor_replace').innerHTML='%s'" %text
            dr.execute_script(js)
            WebDriverWait(dr,100,2).until(lambda x:x.find_element_by_xpath('//*[@id="tb_rich_poster"]/div[3]/div[3]/div/a')).click()
            time.sleep(2)

            print('帖子：'+dr.title+'\n回帖成功')
        except:
            print('错误')

    print('所有发帖完成')
    dr.close()



if __name__ == '__main__':
    html =  input('请输入网址\n>>>')
    username = input('输入用户名\n>>>')
    password = input('输入密码\n>>>')
    text = input('输入发帖内容\n>>>')
    print('获取每个帖子地址\n.............')
    tz = url(html)
    print(tz)
    print('获取完成开始发帖\n')
    login(tz,username,password,text,html)