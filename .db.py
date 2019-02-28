import mysql.connector

host = ""
user = ""
passwd = ""
database = ""
def create_conn():
    maxdb = mysql.connector.connect(
      host = host,
      user = user,
      password = passwd,
      database = database,
      )
    return maxdb.cursor()
