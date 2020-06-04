import requests
import os
import re
import json
from mysql import insert
from lxml import etree
res = requests.Session()

cookie_text = 'cookie.txt'
class taobao_spider:
    def __init__(self,from_data):


        self.from_data = from_data   #登录请求信息

        self.login_url = 'https://login.taobao.com/newlogin/login.do?appName=taobao&fromSite=0'  #登录页面

        self.i_taobao_url = 'https://s.taobao.com/search?q='

        self.headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36',
            'Content-Type': 'application/x-www-form-urlencoded',
        }

    def _get_cookie(self):
        '''
        登录获取cookies 并保存
        :return:
        '''
        if self._verify_cookies():
            return True
        try:
            response = res.post(self.login_url,data=self.from_data)
            response.raise_for_status()
        except Exception as e:
            print('获取失败{}'.format(e))
            raise e
        redirect = response.json()['content']['data']['redirect']
        if redirect == True:
            print('成功获取cookies')
            self._save_cookies()
        else:
            raise RuntimeError('用户名密码验证失败！response：{}'.format(response.text))

    def _verify_cookies(self):
        '''
        验证是否有保存的cookies 以及保存的cookie是否过期
        :return:
        '''
        if not os.path.exists(cookie_text):
            return False

        res.cookies = self._load_cookies()

        try:
            self._is_login()
        except Exception as e:
            os.remove(cookie_text)
            print('cookies过期，删除cookies文件！')
            return False
        print('成功加载cookies，登录成功!!!')
        return True
    def _save_cookies(self):
        '''
        存储cookie
        :return:
        '''
        cookies_dict = requests.utils.dict_from_cookiejar(res.cookies)
        with open(cookie_text,'w+', encoding='utf-8') as file:
            json.dump(cookies_dict, file)
            print('保存cookies文件成功！')

    def _load_cookies(self):
        '''
        加载cookies
        :return:  cookies
        '''
        with open(cookie_text, 'r+', encoding='utf-8') as file:
            cookies_dict = json.load(file)
            cookies = requests.utils.cookiejar_from_dict(cookies_dict)
            return cookies

    def _is_login(self):

        '''
        判断是否登录
        :return:
        '''

        response=res.get(self.i_taobao_url)
        username = re.search(r'<input id="mtb-nickname" type="hidden" value="(.*?)"/>', response.text)
        if username:
            print('登录成功用户名为{}'.format(username.group(1)))
            return True
        else:
            raise RuntimeError('未获取到昵称登录失败')

    def search_items(self):
        self._get_cookie()
        item_name = input('请输入商品名称')
        while True:
            item_page = input('请输入爬取的页数最大100')

            try:
                page = int(item_page)
                if page > 0 and page < 100:
                    break
                else:
                    print('请输入正确页数')
            except:
                print('请输入数字')


        for i in range(page):
            url = 'https://s.taobao.com/search?q='+ item_name + '&s=' +str(page*44)
            req = res.get(url,headers=self.headers,)
            item_dict = {}

            items_data = re.findall(r'{"i2iTags".*?,"risk":""}',req.text)

            for data in items_data:
                data = json.loads(data)  #序列化data 消除=格式错误
                detail_url = data['detail_url']
                title = data['raw_title']
                view_price = data['view_price']
                nick = data['nick']
                comment_count =data['comment_count']
                values = "'{}'," * 4 + "'{}'"
                values = values.format(title,nick,detail_url,view_price,comment_count)
                sql = 'insert into tb_items (title,nick,detail_url,view_price,comment_count) values ({})'.format(values)
                insert(sql)





if __name__ == '__main__':
    from_data = {'loginId': '449681077@qq.com',
                 'password2': '1e6a42512131b27fe6ca16dbbc5b50727b98d9e22d75c8acd3b7230eb0668768d8fdb7dfcf9d3d0f5cc720846f1a96d0b0a488aa98ee446d51fd7476151117128e27e136eb6b2ec240cea7925c475a55f1f60fa4832455181191beaba2aeae2853d1e1aedf9e43abbd01d911fd9872168b9e42c1c16f7b3742b1fe4cc35ec5a7',
                 'keepLogin': 'false',
                 'ua': '124#4IDYlx7NxG0xA5iXTcjCb2FzyW4pSPsl5FZqtPH4TZFQPAj7Nuje7Lt0iogpw/1cXl7ySa1feLDUALV3ftW2+sL7nFumrswEJqtjsoETSd1Vt0pRxUtsvHVRqaZi+jICDKmYADxLPDMB46StecoLzXwyYwRA5JXpxEqv6Abtq9+Rv91aIxaKPLbwwWT9cfY+8QMDdtxI/kFfGRmEJCAndPgd6wLxskg577eK9VwPeWkStCzdzHOY+YRkM1ptYyR6lZ8oKejVX2LJSOFhNGnCATyuWt0N7exkWgw1/7jbk+7hT2dxvdFb1yTB023Vd253ggOlW2EvmlrwpostFFpqFBuhY5U7UyEeO0XHInYLbmYIm4WZIqXp6TF4BMCVtFY2g7OHJCYplmi19jrUJ8Lpg91d1ZIZbU7ng7OBInYLlwYnmfWeIqsXgTzo1nIelUX2g7vtIn/plw/nm4+ZI8LLgTGl7Zm9yq/2DbOBIZzjw5EGvfCzI8XbcPzo1n/0AeUv5j5cDZ3BYZ4GO/sfQq3mIiVehewHKvZ9Ceb8fES0mSIRBydkCQkGKpOiR4Ykb8eE3rmUZ4k7b8WUSi92vOwNzp7vxo+GrOzBgDktZwcY6D59fFzpY3a4zDixSzpgUgDPGz2j/+R/tS1FNLxysdg/g2pG0LNVSv8MawxK7FkPvIa78xnYBQPoJJgUK3KlI0ET4WST2qR4B7CQ23Dedu5btP06ECmWRPFtUFtiaNQBBryu9bO5HmQkbdXoy9AX5ymGgQR0iBEMyEpf36f/eeDj2PzY8bwRtsU0J1LMxc+MOxGgam7J1pJtyeLOJ5C+IIm0eDauH/fGXHu0HYe/1x3JGcgkJ+C9v0RKu337hurWNu4CUxN9RWUetL7EnzlO93Gjn/9K6mDqhKZ5JmvCwIltoq+1W6Qo4gaaNL70/XP+5IcpEVbwwaJFDz41UcwtDyE17bwRX+kq8QX7GQfrZbP5vq5yPLxmRz0EYAqFCgcyUN1HQdDVSASKrfCaxBY27n1E+YGmAZBHDgU/ojz323WNJrpNXzRPdvVTunwHAX2LR5XiyVNVlEnKsLfYVQz9vYs0duEdpMzWt+Uc8of8wk1kvn7HPzTniVkacSBmOs0OnAvLBITQilZG9zIrhtuvqLqmXb9F2wNdv65ocxCqAHyH9pTQ/HX7pdda2jYJFQbIgitN3Izz1AKainjTd8SLtJXErJAuArHQbdgUgViXNvjIgP/uTBq+cEZvyMkGkgmz',
                 'umidGetStatusVal': '255', 'screenPixel': '2560x1440', 'navlanguage': 'zh-CN',
                 'navUserAgent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36',
                 'navPlatform': 'Win32', 'appName': 'taobao', 'appEntrance': 'taobao_pc',
                 '_csrf_token': 'bjYvX3Jj1v1df6YpmXIMt', 'umidToken': '8fcb2b1f3edb27795db0ef68c3bfe400fb97c5c1',
                 'hsiz': '186da8ade7eae924c872ac4e0bd890b9', 'style': 'default', 'appkey': '00000000',
                 'from': 'tbTop', 'isMobile': 'false', 'lang': 'zh_CN', 'fromSite': '0'}
    tb = taobao_spider(from_data=from_data)

    tb.search_items()