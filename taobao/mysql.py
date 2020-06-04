import pymysql
def insert(sql):
    conn = pymysql.connect(host='localhost',
                           user='root',
                           password='santbbd',
                           db='test',
                           charset='utf8')
    cursor = conn.cursor()
    try:
        cursor.execute(sql)
        conn.commit()
    except Exception as e:
        print(e)