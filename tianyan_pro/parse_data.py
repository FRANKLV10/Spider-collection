import sql_func
import detail_info
import datetime

def mysql_parse(tableName,time):
    '''
    解析数据库中存的数据
    :param tableName: 表名
    :param time :时间
    :return:
    '''
    jsons = sql_func.get_json(time) #解析数据库中的json

    for i in jsons:
        try:
            dic = eval(i[0])
            dic_company = detail_info.company_base_info(dic)  # 解析company_base_info

        # dic_contact = detail_info.company_contact_info(i[0]) #解析company_contact_info

            sql_func.InsertData(tableName,dic_company)
        except:
            with open('err_data.txt','a',encoding='utf8') as file:
                file.write(str(dic)+'\n')
                file.close()
        # save.InsertData("company_contact",dic_contact)
def parse_now(dic, tableName):
    '''
        爬取时直接解析
        :param dic: json数据
        :param tableName: 插入的表名称
        :return:
    '''

    dic_company = detail_info.company_base_info(dic)
    # dic_contact = detail_info.company_contact_info(dic)

    sql_func.InsertData(tableName, dic_company)



if __name__ == '__main__':
    begin = datetime.date(2012, 1, 1)
    end = datetime.date(2019, 12, 31)
    print("开始解析")
    for i in range((end - begin).days + 1):

        day = begin + datetime.timedelta(days=i)
        day = str(day)
        daytime = day

        mysql_parse('company',daytime)


    print('完成')
