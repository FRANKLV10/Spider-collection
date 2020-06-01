import logging
import traceback
import time
import pymysql

log_time = time.strftime('%Y-%m-%d', time.localtime(time.time()))
logging.basicConfig(filename='./log/' + str(log_time) + 'err_log.txt', level=logging.WARNING,
                    format='%(asctime)s - %(levelname)s - %(message)s')
def InsertData(TableName,dic):
    """
    只要是字典类型数据可以直接存储
    @param TableName: 表名
    @param dic: 字典数据
    """
    try:
        conn = pymysql.connect(host='localhost', user='root', passwd='123456', db='tianyancha', port=3306,
                               charset="utf8")  # 链接数据库
        cur = conn.cursor()
        COLstr = ''
        ROWstr = ''
        ColumnStyle =  ' TEXT'

        for key in dic.keys():
            COLstr = COLstr + ' ' + key +','
            COLstrEs = COLstr + ' ' + key + ColumnStyle+','
            ROWstr = (ROWstr + '"%s"' + ',') % (dic[key])
        # print(COLstr)
        # print(ROWstr)
        try:
            cur.execute("INSERT  INTO %s (%s) VALUES (%s)" % (TableName,COLstr[:-1], ROWstr[:-1]))

            # 尝试插入如果没有表先创建
        except pymysql.Error as e:

            cur.execute("CREATE TABLE %s (%s)  DEFAULT CHARSET=utf8;" % (TableName, COLstrEs[:-1]))
            cur.execute("INSERT  INTO %s (%s) VALUES (%s)" % (TableName,COLstr[:-1], ROWstr[:-1]))
        conn.commit()
        cur.close()
        conn.close()
    except pymysql.Error as e:
        logging.error(traceback.format_exc())
        print("Mysql Error %d: %s" % (e.args[0], e.args[1]))
        with open('err_dic.txt', 'a', encoding='utf8') as file:
            file.write(str(dic) + '\n')
            file.close()

def save_json(data,daytime):
    """

    @param data: json串
    @param daytime: 企业注册的时间方便二次处理时查询
    """
    try:
        conn = pymysql.connect(host='localhost', user='root', passwd='123456', db='tianyancha', port=3306,
                               charset="utf8")  # 链接数据库
        cur = conn.cursor()
        values ='"'+ str(daytime)+'","'+str(data)+'"'



        try:

            cur.execute('''INSERT INTO COMPANY_DATA (es_time,data_dict) VALUES (%s)''' % values)
            
        except pymysql.Error as e:
            print("Mysql Error %d: %s" % (e.args[0], e.args[1]))
            with open('err_data.txt','a',encoding='utf8') as file:
                file.write(values+'\n')
                file.close()


        conn.commit()
        cur.close()
        conn.close()

    except pymysql.Error as e:
        logging.error(traceback.format_exc())
        print("Mysql Error %d: %s" % (e.args[0], e.args[1]))



def get_json(time):
    '''

    @param time: 查询指定注册时间的企业
    @return:
    '''
    try:
        conn = pymysql.connect(host='localhost', user='root', passwd='123456', db='tianyancha', port=3306,
                               charset="utf8")  # 链接数据库
        cur = conn.cursor()


        try:

            cur.execute('select data_dict from COMPANY_DATA where es_time = %s' %('"'+time+'"'))

            result = cur.fetchall()

            return result

        except pymysql.Error as e:
            print("Mysql Error %d: %s" % (e.args[0], e.args[1]))

        conn.commit()
        cur.close()
        conn.close()

    except pymysql.Error as e:
        logging.error(traceback.format_exc())
        print("Mysql Error %d: %s" % (e.args[0], e.args[1]))

