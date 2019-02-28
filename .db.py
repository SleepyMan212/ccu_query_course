import pymysql

host = ""
user = ""
passwd = ""
database = ""
def create_conn():
    maxdb = pymysql.connect(
      host = host,
      user = user,
      password = passwd,
      database = database,
      )
    return maxdb
