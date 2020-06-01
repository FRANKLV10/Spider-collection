import time
import sql_func
import cover_data


def convert_time(Num): # 转换时间格式
    Num =int(Num)
    timeTemp = float(Num / 1000)
    tupTime = time.localtime(timeTemp)
    standardTime = time.strftime("%Y-%m-%d %H:%M:%S", tupTime)
    return standardTime

def company_base_info(dic):
    '''
    公司基本信息
    :param dic:
    :return:
    '''
    try:

        base_info = {}
        base_kv_data = {'COMPANY_ID': 'id', 'COMPANY_NAME': 'name', 'HISTORY_NAME': 'historyNames',
                   'REG_LOCATION': 'regLocation', 'COMPANY_ORG_TYPE': 'oriCompanyOrgType',
                   'ORG_NUMBER': 'orgNumber', 'REG_INSTITUTE': 'regInstitute', 'ESTABLISH_TIME': 'establishTime',
                   'FROM_TIME': 'fromTime', 'TO_TIME': 'toTime', 'APPROVED_TIME': 'approvedTime','SCORE': 'score',
                   'LEGAL_PERSON_NAME': 'legalPersonName', 'PROVINCE': 'base', 'CITY': 'city', 'REG_CAPITAL': 'regCapital',
                   'REG_CAPITAL_TYPE': 'regCapitalCurrency', 'REG_CAPITAL_NUM': 'paramRegCapital',
                   'ACT_CAPITAL': 'ActCapital', 'ACT_CAPITAL_NUM': 'paramActCapital',
                   'REG_NUMBER': 'regNumber', 'CREDIT_CODE': 'creditCode', 'REG_STATUS': 'paramRegStatus',
                   'BUSINESS_SCOPE': 'businessScopeSws','UPDATE_TIME': 'crawlTime','SOCIAL_SECURITY_STAFF_NUM':'socialSecurityStaffNum',
                    'AREA':'','INDUSTRY':'','DIY_LOCATION':'','AREA_CODE':'areaCode',}
        for key,value in base_kv_data.items():

            try:
                if  key == 'SOCIAL_SECURITY_STAFF_NUM' and dic[value] =='0':
                    base_info[key] = '未公开'
                elif '_TIME' in key and 'Time' in value:
                    base_info[key] = convert_time(dic[value])

                elif key == 'AREA':
                    base_info['AREA'] = cover_data.get_area(dic["areaCode"])
                elif key == 'DIY_LOCATION':

                    if '天府新区' in dic["regLocation"] or '天府新区' in dic["regInstitute"]:
                        base_info['DIY_LOCATION'] = '天府新区'

                    elif '高新区' in dic["regLocation"] or '高新' in dic["regInstitute"]:
                        base_info['DIY_LOCATION'] = '高新区'
                    else:
                        base_info['DIY_LOCATION'] = cover_data.get_area(dic["areaCode"])

                elif key =='INDUSTRY':
                    base_info['INDUSTRY'] = cover_data.get_industry(dic["companyCate1"], dic["companyCate2"])
                else:
                    base_info[key] = dic[value]
            except:
                if key == 'TO_TIME':
                    base_info[key] = '无固定期限'
                else:
                    base_info[key] ='未公开'


        return base_info
    except:
         with open('err_dic.txt', 'a', encoding='utf8') as file:
            file.write(dic + '\n')
            file.close()


def company_contact_info(dic):
    '''
    公司联系方式
    :param dic:
    :return: dic
    '''
    contact_info = {}
    web_kv_data={'COMPANY_ID': 'id','WEBSITES':'websites', 'MOBILE_PHONE': 'phonesMobile',
               'PHONES': 'phones', 'EMAILS': 'emails','REG_LOCATION': 'regLocation',
                 'UPDATE_TIME': 'crawlTime','website_Names_Noticp':'websiteNamesNoticp'}

    for key, value in web_kv_data.items():
        try:

            if '_TIME' in key and 'Time' in value:
                contact_info[key] = convert_time(dic[value])
            else:
                contact_info[key] = dic[value]
        except:
            contact_info[key] = '未公开'
    return len(contact_info)




if __name__ == '__main__':

    print(convert_time("1585042278162"))
    # print(company_base_info(dic))