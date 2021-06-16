import datetime
import mysql.connector
import conversion as cv

#DB接続
db = mysql.connector.connect(host="localhost", user="root", password="")
cursor = db.cursor(buffered=True)
cursor.execute("use test_db")
db.commit()

def create_sample():
  cursor.execute('select * from taikin where exists (select id from taikin)')
  a = cursor.fetchone()
  cursor.execute('show tables')
  b = cursor.fetchall()
  return b

def now_record():
  date_today = datetime.date.today()
  date_time = datetime.datetime.now()
  date_now = date_time.replace(microsecond = 0)
  year = date_now.year
  month = date_now.month
  day = date_now.day
  hour = date_now.hour
  minute = date_now.minute
  second = date_now.second
  return date_today, date_now, year, month, day, hour, minute, second

def attendance_list():
  #直近5日間の出退勤データ取得
  cursor.execute('select in_time from syukin order by id desc limit 5')
  in_t = cursor.fetchall()
  cursor.execute('select out_time from taikin order by id desc limit 5')
  in_o = cursor.fetchall()
  in_list = []
  for a in zip(in_o,in_t):
    for i in a:
      in_list.append(i)
  return in_list

def working_sum():
  nr = now_record()
  year = nr[2]
  month = nr[3]
  #チェック項目
  cursor.execute('select year,month from taikin order by id desc limit 1')
  check = cursor.fetchone()
  check_year = int(check[0])
  check_month = int(check[1])
  if check_year == year and check_month == month:
    sql = 'select sum(hour),sum(minute),sum(second) from syukin where year = %s and month = %s'
    cursor.execute(sql,(year, month))
    start_time = cursor.fetchone()
    start_hour = int(start_time[0])
    start_minute = int(start_time[1])
    start_second = int(start_time[2])
    sql2 = 'select sum(hour),sum(minute),sum(second) from taikin where year = %s and month = %s'
    cursor.execute(sql2,(year, month))
    end_time = cursor.fetchone()
    end_hour = int(end_time[0])
    end_minute = int(end_time[1])
    end_second = int(end_time[2])
    result_second = end_second - start_second
    result_minute = end_minute - start_minute
    result_hour = end_hour - start_hour
    total_work = cv.conversion_sum(result_second, result_minute, result_hour)
    if total_work[0] >= 180:
      total_str = str(total_work[0]) + ":" + str(total_work[1]) + ":" + str(total_work[2])
      return total_str
    else:
      total_str = str(total_work[0]) + ":" + str(total_work[1]) + ":" + str(total_work[2])
      return total_str

def oversum_calc():
  nr = now_record()
  year = nr[2]
  month = nr[3]
  #チェック項目
  cursor.execute('select year,month from zangyo order by id desc limit 1')
  check = cursor.fetchone()
  check_year = int(check[0])
  check_month = int(check[1])
  if check_year == year and check_month == month:
    cursor.execute('select sum_time from zangyo order by id desc limit 1')
    total = cursor.fetchone()
    total_int = cv.conversion_time(total[0])
    if total_int[0] >= 80:
      total_str = str(total_int[0]) + ":" + str(total_int[1]) + ":" + str(total_int[2])
      message = "Overtime hours exceeded 80 hours!!"
      return total_str, message
    elif total_int[0] >= 45:
      total_str = str(total_int[0]) + ":" + str(total_int[1]) + ":" + str(total_int[2])
      message = "Overtime hours exceeded 45 hours!!"
      return total_str, message
    else:
      total_str = str(total_int[0]) + ":" + str(total_int[1]) + ":" + str(total_int[2])
      return total_str
  else:
    nothing = " Nothing "
    return nothing

def stamping_in():
  nr = now_record()
  cursor.execute("insert into syukin (in_day, in_time, year, month, day, hour, minute, second) values (%s, %s, %s, %s, %s, %s, %s, %s)",(nr[0], nr[1], nr[2], nr[3], nr[4], nr[5], nr[6], nr[7]))
  db.commit()
  return nr

def stamping_out():
  nr = now_record()
  cursor.execute("insert into taikin (out_day, out_time, year, month, day, hour, minute, second) values (%s, %s, %s, %s, %s, %s, %s, %s)",(nr[0], nr[1], nr[2], nr[3], nr[4], nr[5], nr[6], nr[7]))
  db.commit()
  return nr

def overtime_calc():
  #直近退勤時間の取得
  cursor.execute('select out_day,out_time from taikin order by id desc limit 1')
  date_out = cursor.fetchone()
  date_today = date_out[0]
  date_now = date_out[1]
  #残業開始時間の定義
  over_start = date_now.replace(hour=17, minute=45, second=00)
  year = date_now.year
  month = date_now.month
  day = date_now.day
  #当日の残業時間換算
  over_day = date_now - over_start #datetime型にて計算
  over_second = int(over_day.total_seconds()) #timedelta型を総秒数に変換,over_timeカラム
  time_table = cv.conversion_time(over_second) #総秒数をint型へ変換
  hour = time_table[0]
  minute = time_table[1]
  second = time_table[2]

  #直近の残業日付取得
  cursor.execute('select over_day,sum_time from zangyo order by id desc limit 1')
  nearest = cursor.fetchone()
  nearest_year = nearest[0].year
  nearest_month = nearest[0].month
  #累計残業時間処理, ifは当月内、elseは月跨ぎ処理
  if nearest_year == year and nearest_month == month:
    over_sum = int(nearest[1]) + over_second
    time_table = cv.conversion_time(over_sum) #総秒数をint型へ変換
    cursor.execute("insert into zangyo (over_day, over_time, year, month, day, hour, minute, second, sum_time) values (%s, %s, %s, %s, %s, %s, %s, %s, %s)",(date_today, over_second, year, month, day, hour, minute, second, over_sum))
    db.commit()
    return over_second
  else:
    cursor.execute("insert into zangyo (over_day, over_time, year, month, day, hour, minute, second, sum_time) values (%s, %s, %s, %s, %s, %s, %s, %s, %s)",(date_today, over_second, year, month, day, hour, minute, second, over_second))
    db.commit()
    #result = "bbb"
    return over_second