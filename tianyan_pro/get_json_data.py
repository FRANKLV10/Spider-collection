import requests
import json
import datetime
import sql_func
from parse_data import parse_now
import time
import sys
import traceback
import logging


def post_data(headers,from_data,day,page):
    log_time = time.strftime('%Y-%m-%d', time.localtime(time.time()))
    logging.basicConfig(filename='./log/' + str(log_time) + 'err_log.txt', level=logging.WARNING,
                        format='%(asctime)s - %(levelname)s - %(message)s')   #日志记录地址、级别等设置
    try:
        re = requests.post('https://std.tianyancha.com/cloud-search-company/company/screen.json', data=from_data,
                           headers=headers)
        if re.text == None:
            print("账号被锁定或cookies过期程序终止于" + day + "第" + page + "页")
            sys.exit(0)
        else:
            text = json.loads(re.text)
            return text['data']['items']

    except Exception as e:
        print('发生错误的文件：', e.__traceback__.tb_frame.f_globals['__file__'])

        print('错误信息', e,)

        if e == 'Expecting value: line 1 column 1 (char 0)':
            print('账号被锁定或cookies过期程序终止于" + day + "第" + page + "页"')
            sys.exit(1)
        logging.error(traceback.format_exc())
        with open('err_day.txt', 'a', encoding='utf8') as file:
            file.write(day + ' ' + page + '\n')
            file.close()



def json_info():
    '''
    获取天眼查高级搜索模式下公司json
    from_data :具体kv天眼查专业版高级搜索之后浏览器f12 xhr中查看做出适当修改
    部分kv注释
            'sortStr': '{"param_reg_capital": "desc"}', #注册 资金降序
            'regCapGte': '100', #注册资金最小为
            'regStatOr': '1 2', #企业状态 1 2 为 在业存续
            'isComAndBusScope': '1',
            'cat2Or':'62', #二级行业
            'companyTypeOr': '1', # 公司类型所有
            'regDateGte': "19000101", #起始日期
            'regDateLte': "20201231",#截至日期
            'hasMobile': '2',
            'cat3Or': '794', #三级行业
            'pn': page, #页数
            'ps': '50', #一页显示个数
            'areaCode2Or': '5101', #二级区域
            'cat1Or': 'F', # 一级行业代码
            'comAnd': '超市' #关键字
    '''
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'keep-alive',
        'Content-Length': '749',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Cookie': 'TYCID=b0d81ab0628011ea9068576c9a359aa1; undefined=b0d81ab0628011ea9068576c9a359aa1; ssuid=7039631112; _ga=GA1.2.267575536.1583811546; tyc-user-phone=%255B%252215108389554%2522%255D; CLOUDID=83c9c02b-efd6-4491-ab64-d2d65537b3f3; parent_qimo_sid_f0615f20-d9d7-11e9-96c6-833900356dc6=a24fad60-6347-11ea-a49b-11a674d348b6; jsid=SEM-BAIDU-PZ2003-VI-000001; bad_idf0615f20-d9d7-11e9-96c6-833900356dc6=b473dcd1-6817-11ea-86ec-5d3b2603a5c7; Hm_lvt_e92c8d65d92d534b0fc290df538b4758=1586398873,1586401817,1586401921,1586997818; tyc-user-info=%257B%2522claimEditPoint%2522%253A%25220%2522%252C%2522vipToMonth%2522%253A%2522false%2522%252C%2522explainPoint%2522%253A%25220%2522%252C%2522integrity%2522%253A%252210%2525%2522%252C%2522state%2522%253A%25225%2522%252C%2522surday%2522%253A%2522272%2522%252C%2522announcementPoint%2522%253A%25220%2522%252C%2522bidSubscribe%2522%253A%2522-1%2522%252C%2522vipManager%2522%253A%25220%2522%252C%2522onum%2522%253A%252267%2522%252C%2522monitorUnreadCount%2522%253A%25220%2522%252C%2522discussCommendCount%2522%253A%25220%2522%252C%2522claimPoint%2522%253A%25220%2522%252C%2522token%2522%253A%2522eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiIxNTEwODM4OTU1NCIsImlhdCI6MTU4Njk5NzgyOCwiZXhwIjoxNjE4NTMzODI4fQ.NZzn-PXwlUasmP8msd7rnXVwL1SSrcwTIj4QgtpJ_mN0PCT8K4saGKHCX0t1DiVslFdNSg3-GH8Zp83-BDLdaw%2522%252C%2522vipToTime%2522%253A%25221610420864948%2522%252C%2522redPoint%2522%253A%25220%2522%252C%2522myAnswerCount%2522%253A%25220%2522%252C%2522myQuestionCount%2522%253A%25220%2522%252C%2522signUp%2522%253A%25220%2522%252C%2522nickname%2522%253A%2522%25E5%25B0%25BC%25E5%25B0%2594%25E6%2596%25AF%25C2%25B7%25E7%258E%25BB%25E5%25B0%2594%2522%252C%2522privateMessagePointWeb%2522%253A%25220%2522%252C%2522privateMessagePoint%2522%253A%25220%2522%252C%2522isClaim%2522%253A%25220%2522%252C%2522isExpired%2522%253A%25220%2522%252C%2522pleaseAnswerCount%2522%253A%25220%2522%252C%2522bizCardUnread%2522%253A%25220%2522%252C%2522vnum%2522%253A%252220%2522%252C%2522mobile%2522%253A%252215108389554%2522%257D; auth_token=eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiIxNTEwODM4OTU1NCIsImlhdCI6MTU4Njk5NzgyOCwiZXhwIjoxNjE4NTMzODI4fQ.NZzn-PXwlUasmP8msd7rnXVwL1SSrcwTIj4QgtpJ_mN0PCT8K4saGKHCX0t1DiVslFdNSg3-GH8Zp83-BDLdaw; bad_id658cce70-d9dc-11e9-96c6-833900356dc6=6e799c31-7f7b-11ea-880a-7d57c984e976; aliyungf_tc=AQAAAKUXnSxyZwMAiv/UqyZtVWwaJdes; csrfToken=pzMFuBWh-kvjCjzk6zziv4mx; Hm_lvt_dfd2445765658d46619739a80fb5f6b2=1587516387,1587693942,1588055700,1588208417; X-TOKEN=eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ7XCJjcmVhdGVUaW1lXCI6MTU4ODIwODQyNjk3MixcImV4cGlyZXNcIjo2MDQ4MDAsXCJpZFwiOjExODE1MzksXCJtb2JpbGVcIjpcIjE2NTczOTczNDUyXCIsXCJvcmRlcklkXCI6MjUzNTEsXCJvcmdJZFwiOjI2MjkwLFwicHJvSWRcIjozMzA0LFwidXNlcklkXCI6ODY1OTk4LFwidXNlcm5hbWVcIjpcIjE2NTczOTczNDUyXCIsXCJ2cG5cIjpmYWxzZX0iLCJqdGkiOiIxMTgxNTM5IiwiaXNzIjoic3RkLnRpYW55YW5jaGEuY29tIiwibmJmIjoxNTg4MjA4NDI2LCJpYXQiOjE1ODgyMDg0MjYsImV4cCI6MTU4ODgxMzIyNn0.MV2RbOR7lT9R-ghCNX3ZLG0m7vOLsCx7AVrOIsU81Qw; UID=865998; UNAME=16573973452; UORG=26290; qimo_seosource_f0615f20-d9d7-11e9-96c6-833900356dc6=%E7%AB%99%E5%86%85; qimo_seokeywords_f0615f20-d9d7-11e9-96c6-833900356dc6=; href=https%3A%2F%2Fstd.tianyancha.com%2Fhome; accessId=f0615f20-d9d7-11e9-96c6-833900356dc6; pageViewNum=1; nice_idf0615f20-d9d7-11e9-96c6-833900356dc6=fcba8a11-8a7d-11ea-97fb-e5908bcaecf8; Hm_lpvt_dfd2445765658d46619739a80fb5f6b2=1588208449',        'Sec-Fetch-Dest': 'empty',
        'Origin': 'https://std.tianyancha.com',
        'Referer': 'https://std.tianyancha.com/searchx?pn=1&ps=15&pn=1&ps=15&combus=1&ctypeor=1&hasm=2&ismat=1&ht=2&ipam=1&hm=2&hrl=2&hr=2&htm=2&hw=2&hp=2&hd=2&isht=2&islist=2&hls=2&hca=2&het=2&hrr=2&hja=2&hab=2&hph=2&hil=2&heq=2&htc=2&hep=2&hevp=2&hjs=2&hcl=2&hip=2&hzp=2&htcl=2&hl=2&hie=2&hws=2&hc=2&mg=2&c1or=&c2or=&regcg=1000&regcl=90000000&sortkey=establish_time&sortval=desc&regdg=20200101&regdl=20200316',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'ors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36',
        'version': 'TYC-STD',
        'x-csrf-token': '4qOxDlSSTWmRmMAJyeIzdDJF',
    }
    begin = datetime.date(2018, 1, 1)               #设置要爬取的日期
    end = datetime.date(2018, 12, 31)
    for i in range((end - begin).days + 1):
        day = begin + datetime.timedelta(days=i)
        day = str(day)
        daytime = day
        day = day.replace("-", "")
        for j in range(1, 100):
            page = str(j)
            from_data = {

                'isComAndBusScope': '1',
                'comCategoryOr': '0 1 2 3 4 6 7 8 9 10 11 12',
                # 'comCategoryOr': '1',
                'regDateGte': day,
                'regDateLte': day,
                'hasMobile': '2',
                'isMobileAndTelephone': '0',
                'isHighTech': '2',
                'isListed': '2',
                'hasLawsuit': '2',
                'hasCourtAnnouncement': '2',
                'hasExecuted': '2',
                'hasRestriction': '2',
                'hasJudicialaAid': '2',
                'hasAbnormal': '2',
                'hasPunishment': '2',
                'hasIllegal': '2',
                'hasEquity': '2',
                'hasTaxContraventions': '2',
                'hasEquityPledge': '2',
                'hasEnvironmentalPenalties': '2',
                'hasJudicialSale': '2',
                'hasClearing': '2',
                'hasIntellectualProperty': '2',
                'hasBaipin': '2',
                'hasTeleCommunicationLicense': '2',
                'hasLicense': '2',
                'hasImportAndExport': '2',
                'hasTelephone': '2',
                'isPhoneAndMail': '0',
                'hasMail': '2',
                'hasRegLoc': '2',
                'hasRound': '2',
                'hasTm': '2',
                'hasPatent': '2',
                'hasDishonest': '2',
                'hasCopyrightWorks': '2',
                'hasWebsites': '2',
                'hasCopyright': '2',
                'hasMortgage': '2',
                'pn': page,
                'ps': '50',         #每页显示多少家公司，默认15， 50 减少请求次数
                'areaCode2Or': '5101', # 二级区域代码，
            }

            data = post_data(headers,from_data,day,page)

            if data == None:
                if j == 1:
                    print(daytime + "无更新")
                else:
                    print(daytime + '爬取完成')
                break
            else:
                for dic in data:


                    try:
                        sql_func.save_json(dic, daytime)  #爬取json 格式数据存储
                        # parse_now(dic, 'company')   #直接解析
                    except:
                        with open('err_dic.txt', 'a', encoding='utf8') as file:
                            file.write(dic + '\n')
                            file.close()

                time.sleep(0.5)

        time.sleep(2)



if __name__ == '__main__':
    json_info()