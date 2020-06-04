import pymysql
def insert(sql):
    conn = pymysql.connect(host='localhost',
                           user='root',
                           password='123456',
                           db='test',
                           charset='utf8')
    cursor = conn.cursor()
    try:
        cursor.execute(sql)
        conn.commit()
    except Exception as e:
        print(e)
