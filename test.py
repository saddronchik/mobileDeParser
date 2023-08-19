import pymysql

try:
    connection = pymysql.connect(
        host='localhost',
        port=3306,
        user='root',
        database='encar',
        cursorclass=pymysql.cursors.DictCursor)
    
    print('success')

except Exception as ex:
    print(ex)