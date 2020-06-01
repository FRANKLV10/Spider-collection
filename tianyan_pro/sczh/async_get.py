import requests
import logging
import asyncio

import aiohttp
from sczh import db_mysql
from bs4 import BeautifulSoup
from sczh import catch
import re
import time

day = time.strftime('%Y-%m-%d', time.localtime(time.time()))
logging.basicConfig(filename='./log/' + str(day) + 'err_log.txt', level=logging.WARNING,
                    format='%(asctime)s - %(levelname)s - %(message)s')


def spend_time(time_func):
    def func(*args, **kwargs):
        start = time.time()
        time_func(*args, **kwargs)
        end = time.time()
        print("花费的时间：" + str(end - start))

    return func


async def get_htm(id):
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Cookie': 'TYCID=b0d81ab0628011ea9068576c9a359aa1; undefined=b0d81ab0628011ea9068576c9a359aa1; ssuid=7039631112; _ga=GA1.2.267575536.1583811546; tyc-user-phone=%255B%252215108389554%2522%255D; CLOUDID=83c9c02b-efd6-4491-ab64-d2d65537b3f3; parent_qimo_sid_f0615f20-d9d7-11e9-96c6-833900356dc6=a24fad60-6347-11ea-a49b-11a674d348b6; jsid=SEM-BAIDU-PZ2003-VI-000001; bad_idf0615f20-d9d7-11e9-96c6-833900356dc6=b473dcd1-6817-11ea-86ec-5d3b2603a5c7; aliyungf_tc=AQAAAJVvqAzbQwsAqOpZ2rMqOX14e7uj; csrfToken=Y8y9xvyOXOF9lDgUIiR_O6O-; Hm_lvt_dfd2445765658d46619739a80fb5f6b2=1585536438; X-TOKEN=eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ7XCJjcmVhdGVUaW1lXCI6MTU4NTUzNjk2MzQ5MCxcImV4cGlyZXNcIjo2MDQ4MDAsXCJpZFwiOjEwNDQ4NDYsXCJtb2JpbGVcIjpcIjE3MTM1MTkyODU1XCIsXCJvcmRlcklkXCI6MjQ2MjIsXCJvcmdJZFwiOjI1NTY3LFwicHJvSWRcIjozMzA0LFwidXNlcklkXCI6ODY0NzUxLFwidXNlcm5hbWVcIjpcIjE3MTM1MTkyODU1XCIsXCJ2cG5cIjpmYWxzZX0iLCJqdGkiOiIxMDQ0ODQ2IiwiaXNzIjoic3RkLnRpYW55YW5jaGEuY29tIiwibmJmIjoxNTg1NTM2OTYzLCJpYXQiOjE1ODU1MzY5NjMsImV4cCI6MTU4NjE0MTc2M30.hSkmiV5bDHpWYhLU52qQz3-KA_I55x7Wj5TyACMdH9M; UID=864751; UNAME=17135192855; UORG=25567; qimo_seosource_f0615f20-d9d7-11e9-96c6-833900356dc6=%E7%AB%99%E5%86%85; qimo_seokeywords_f0615f20-d9d7-11e9-96c6-833900356dc6=; href=https%3A%2F%2Fstd.tianyancha.com%2Fhome; accessId=f0615f20-d9d7-11e9-96c6-833900356dc6; pageViewNum=1; nice_idf0615f20-d9d7-11e9-96c6-833900356dc6=001c08f1-7232-11ea-a6b8-8d8d788bfa0f; Hm_lpvt_dfd2445765658d46619739a80fb5f6b2=1585536975',
        'Referer': 'https://std.tianyancha.com/searchx?pn=1&ps=15&pn=1&ps=15&combus=1&ctypeor=1&hasm=2&ismat=1&ht=2&ipam=1&hm=2&hrl=2&hr=2&htm=2&hw=2&hp=2&hd=2&isht=2&islist=2&hls=2&hca=2&het=2&hrr=2&hja=2&hab=2&hph=2&hil=2&heq=2&htc=2&hep=2&hevp=2&hjs=2&hcl=2&hip=2&hzp=2&htcl=2&hl=2&hie=2&hws=2&hc=2&mg=2&c1or=&c2or=&regcg=1000&regcl=90000000&sortkey=establish_time&sortval=desc&regdg=20200101&regdl=20200316',
        'DNT': '1',
        'Host': 'std.tianyancha.com',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'
    }
    url = "https://std.tianyancha.com/pagination/invest.xhtml?ps=50pn=1&id=" + id
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as res:
            res.encoding = 'utf8'
            text = await res.text()
            await get_detail(text)


@catch.catch_exception
def get_html(url):
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Cookie': 'TYCID=b0d81ab0628011ea9068576c9a359aa1; undefined=b0d81ab0628011ea9068576c9a359aa1; ssuid=7039631112; _ga=GA1.2.267575536.1583811546; tyc-user-phone=%255B%252215108389554%2522%255D; CLOUDID=83c9c02b-efd6-4491-ab64-d2d65537b3f3; parent_qimo_sid_f0615f20-d9d7-11e9-96c6-833900356dc6=a24fad60-6347-11ea-a49b-11a674d348b6; jsid=SEM-BAIDU-PZ2003-VI-000001; bad_idf0615f20-d9d7-11e9-96c6-833900356dc6=b473dcd1-6817-11ea-86ec-5d3b2603a5c7; aliyungf_tc=AQAAAJVvqAzbQwsAqOpZ2rMqOX14e7uj; csrfToken=Y8y9xvyOXOF9lDgUIiR_O6O-; Hm_lvt_dfd2445765658d46619739a80fb5f6b2=1585536438; X-TOKEN=eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ7XCJjcmVhdGVUaW1lXCI6MTU4NTUzNjk2MzQ5MCxcImV4cGlyZXNcIjo2MDQ4MDAsXCJpZFwiOjEwNDQ4NDYsXCJtb2JpbGVcIjpcIjE3MTM1MTkyODU1XCIsXCJvcmRlcklkXCI6MjQ2MjIsXCJvcmdJZFwiOjI1NTY3LFwicHJvSWRcIjozMzA0LFwidXNlcklkXCI6ODY0NzUxLFwidXNlcm5hbWVcIjpcIjE3MTM1MTkyODU1XCIsXCJ2cG5cIjpmYWxzZX0iLCJqdGkiOiIxMDQ0ODQ2IiwiaXNzIjoic3RkLnRpYW55YW5jaGEuY29tIiwibmJmIjoxNTg1NTM2OTYzLCJpYXQiOjE1ODU1MzY5NjMsImV4cCI6MTU4NjE0MTc2M30.hSkmiV5bDHpWYhLU52qQz3-KA_I55x7Wj5TyACMdH9M; UID=864751; UNAME=17135192855; UORG=25567; qimo_seosource_f0615f20-d9d7-11e9-96c6-833900356dc6=%E7%AB%99%E5%86%85; qimo_seokeywords_f0615f20-d9d7-11e9-96c6-833900356dc6=; href=https%3A%2F%2Fstd.tianyancha.com%2Fhome; accessId=f0615f20-d9d7-11e9-96c6-833900356dc6; pageViewNum=1; nice_idf0615f20-d9d7-11e9-96c6-833900356dc6=001c08f1-7232-11ea-a6b8-8d8d788bfa0f; Hm_lpvt_dfd2445765658d46619739a80fb5f6b2=1585536975',
        'Referer': 'https://std.tianyancha.com/searchx?pn=1&ps=15&pn=1&ps=15&combus=1&ctypeor=1&hasm=2&ismat=1&ht=2&ipam=1&hm=2&hrl=2&hr=2&htm=2&hw=2&hp=2&hd=2&isht=2&islist=2&hls=2&hca=2&het=2&hrr=2&hja=2&hab=2&hph=2&hil=2&heq=2&htc=2&hep=2&hevp=2&hjs=2&hcl=2&hip=2&hzp=2&htcl=2&hl=2&hie=2&hws=2&hc=2&mg=2&c1or=&c2or=&regcg=1000&regcl=90000000&sortkey=establish_time&sortval=desc&regdg=20200101&regdl=20200316',
        'DNT': '1',
        'Host': 'std.tianyancha.com',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'
    }
    # try:
    re = requests.get(url, headers=headers)
    re.raise_for_status()
    re.encoding = re.apparent_encoding
    return re.text

    # except Exception as e:
    #     print('错误信息', e, )
    #     logging.error(traceback.format_exc())


@catch.catch_exception
def get_id(name):
    url = "https://std.tianyancha.com/search?key=" + name
    text = get_html(url)
    soup = BeautifulSoup(text, 'lxml')
    res_list = soup.find('div', class_='stdResult-list')
    company_info = res_list.find('div', class_='stdResult-item')
    a_tag = company_info.find('a', class_='name')
    company_id = re.findall(r'https://std.tianyancha.com/company/(.*)', a_tag['href'])
    company_id = str(company_id[0])
    print(company_id)
    return company_id
def get_detail1(id):
    print("正在查找" + id)
    url = "https://std.tianyancha.com/pagination/invest.xhtml?ps=50pn=1&id=" + id
    text = get_html(url)
    soup = BeautifulSoup(text, 'lxml')
    data = soup.tbody
    if data != None:
        company_info = {}
        company_id =[]
        company_name = []
        for i in data.find_all('td', class_='jsmark'):
            company_id.append(i['data-key'])
            company_name.append(i['data-name'])
            # company_info[company_name] =company_id
        company_info['company_id']  = company_id
        company_info['company_name'] = company_name
        return company_info



@catch.catch_exception
async def get_detail(text):

    # url = "https://std.tianyancha.com/pagination/invest.xhtml?ps=50pn=1&id=" + id
    # loop = asyncio.get_event_loop()
    # text =loop.run_until_complete(get_htm(url))
    # text = get_htm(url)
    soup = BeautifulSoup(text, 'lxml')
    data = soup.tbody
    if data != None:
        company_info = {}
        company_id = []
        company_name = []
        for i in data.find_all('td', class_='jsmark'):
            company_id.append(i['data-key'])
            company_name.append(i['data-name'])
            # company_info[company_name] =company_id
        company_info['company_id'] = company_id
        company_info['company_name'] = company_name

        return company_info


#
@spend_time
def search_all(name):
    all_id = []
    all_name =[]

    id = get_id(name)

    first_data = get_detail1(id)
    first_list = first_data['company_id']
    first_name = first_data['company_name']
    all_name.extend(first_name)
    print("获取到一级子公司id")
    if first_list != None:
        print("开始获取二级子公司")
        loop = asyncio.get_event_loop()
        tasks = [asyncio.ensure_future(get_htm(i)) for i in first_list]
        tasks = asyncio.gather(tasks)
        loop.run_until_complete(tasks)

        # for i in first_list:
        #     loop = asyncio.get_event_loop()
        #     second_company_data = loop.run_until_complete(get_htm(i))
        #     if second_company_data == None:
        #         pass
        #     else:
        #         second_company_name = second_company_data['company_name']
        #         all_name.extend(second_company_name)
    # for com in all_name:
    #     db_mysql.select(com)
    print(all_name)


if __name__ == '__main__':
    # search_all("187913274")
    # search_all("2310289621")
    # print(get_detail("2310289621"))
    search_all("成都三泰控股集团股份有限公司")


    # print(get_id("成都三泰控股集团股份有限公司"))
