import mysql.connector
import pandas as pd

db = mysql.connector.connect(host=['DB_HOSTNAME'], user=['DB_USERNAME'], password=['DB_PASSWORD'])
#db = mysql.connector.connect(host="localhost", user="root", password="")
cursor = db.cursor()
cursor.execute("use test_db")
db.commit()

def data_write(y, m):
  #SQLよりデータ取得
  sql = 'select year,month,day from syukin where year = %s and month = %s'
  cursor.execute(sql, (y, m))
  r1 = cursor.fetchall()
  sql2 = 'select hour,minute,second from syukin where year = %s and month = %s'
  cursor.execute(sql2, (y, m))
  r2 = cursor.fetchall()
  sql3 = 'select year,month,day from taikin where year = %s and month = %s'
  cursor.execute(sql3, (y, m))
  r3 = cursor.fetchall()
  sql4 = 'select hour,minute,second from taikin where year = %s and month = %s'
  cursor.execute(sql4, (y, m))
  r4 = cursor.fetchall()
  #DataFrame型へ変換
  s1 = pd.Series(conv_day(r1))
  s2 = pd.Series(conv_time(r2))
  s3 = pd.Series(conv_day(r3))
  s4 = pd.Series(conv_time(r4))
  df = pd.DataFrame({'出勤日':s1,'出勤時間':s2,'退勤日':s3,'退勤時間':s4})
  df.to_csv("data.csv")
  return df
def conv_day(day):
    array = []
    for d in day:
        dd = "{0}/{1}/{2}".format(d[0],d[1],d[2])
        array.append(dd)
    return array

def conv_time(time):
    array = []
    for t in time:
        tt = "{0}:{1}:{2}".format(t[0],t[1],t[2])
        array.append(tt)
    return array