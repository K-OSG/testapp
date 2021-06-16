import mysql.connector

#DB接続
db = mysql.connector.connect(host=['DB_HOSTNAME'], user=['DB_USERNAME'], password=['DB_PASSWORD'])
#db = mysql.connector.connect(host="localhost", user="root", password="")
cursor = db.cursor(buffered=True)
cursor.execute("use test_db")
db.commit()
  
#syukinテーブル及びカラムの作成
def db_create():
  cursor.execute("""create table if not exists syukin(
                  id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
                  in_day DATE,
                  in_time DATETIME,
                  year INT,
                  month INT,
                  day INT,
                  hour INT,
                  minute INT,
                  second INT);""")
  #taikinテーブル及びカラムの作成
  cursor.execute("""create table if not exists taikin(
                  id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
                  out_day DATE,
                  out_time DATETIME,
                  year INT,
                  month INT,
                  day INT,
                  hour INT,
                  minute INT,
                  second INT);""")
  #zangyoテーブル及びカラムの作成
  cursor.execute("""create table if not exists zangyo(
                  id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
                  over_day DATE,
                  over_time INT,
                  year INT,
                  month INT,
                  day INT,
                  hour INT,
                  minute INT,
                  second INT,
                  sum_time INT);""")