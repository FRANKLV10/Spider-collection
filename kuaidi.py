import requests
from lxml import etree
from bs4 import BeautifulSoup
import re
import pymysql
import mysql
class KuaiDiWo:
    def __init__(self):
        self.area_dict = {4209: '双流县', 4210: '大邑县', 4211: '崇州市', 4212: '彭州市', 4213: '成华区', 4214: '新津县',
                          4215: '新都区', 4216: '武侯区', 4217: '温江区', 4218: '蒲江县', 4219: '邛崃市', 4220: '郫县',
                          4221: '都江堰市', 4222: '金堂县', 4223: '金牛区', 4224: '锦江区', 4225: '青白江区', 4226: '青羊区',
                          4227: '龙泉驿区'}

        self.base_url = 'http://www.kuaidiwo.cn/dot/index-'

        self.headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36',}

    def get_data(self):
        for area_code,area in self.area_dict.items():

            for j in range(1,100):
                url = self.base_url+str(area_code)+'_'+ str(j) + '.html'
                res = requests.get(url,headers = self.headers)
                if res.status_code == 404:
                    break
                else:
                    self._parse(area,res)

    def _parse(self,area,res):



        soup = BeautifulSoup(res.text,'lxml')

        for details in soup.find_all(class_="net-info"):

            type = details.find('a').get_text()
            name = details.find('strong').get_text()
            data = details.find('p').get_text()

            location = re.findall('网点地址：(.*)派送区域',data)[0]




            values = "'{}'," * 3 + "'{}'"
            values =values.format(name,location,type,area)

            sql = 'insert into kuaidi (name,location,type,area) values ({})'.format(values)
            mysql.insert(sql)







if __name__ == '__main__':
    kuaidi = KuaiDiWo()
    kuaidi.get_data()