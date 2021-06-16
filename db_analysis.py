import mysql.connector
import pandas as pd
import conversion as cv
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

db = mysql.connector.connect(host=['DB_HOSTNAME'], user=['DB_USERNAME'], password=['DB_PASSWORD'])
#db = mysql.connector.connect(host="localhost", user="root", password="")
cursor = db.cursor(buffered=True)
cursor.execute("use test_db")
db.commit()

def conv_yearday(y,m):
    yd = []
    #月日取得
    sql = 'select year,month from syukin where year = %s and month = %s'
    cursor.execute(sql,(y, m))
    t1 = cursor.fetchone()
    d1 = "{0}/{1}".format(t1[0],t1[1])
    yd.append(d1)
    #労働日数取得
    sql2 = 'select count(day) from syukin where year = %s and month = %s'
    cursor.execute(sql2,(y, m))
    t2 = cursor.fetchone()
    d2 = "{0}日".format(t2[0])
    yd.append(d2)
    #総労働時間取得
    sql3 = 'select sum(hour),sum(minute),sum(second) from syukin where year = %s and month = %s'
    cursor.execute(sql3,(y, m))
    st = cursor.fetchone()
    sql2 = 'select sum(hour),sum(minute),sum(second) from taikin where year = %s and month = %s'
    cursor.execute(sql2,(y, m))
    et = cursor.fetchone()
    r_s = int(et[2]) - int(st[2])
    r_m = int(et[1]) - int(st[1])
    r_h = int(et[0])- int(st[0])
    t3 = cv.conversion_sum(r_s, r_m, r_h)
    d3 = "{0}:{1}:{2}".format(t3[0],t3[1],t3[2])
    yd.append(d3)
    #平均労働時間(日)
    t_s = ((t3[0]*3600)+(t3[1]*60)+t3[2])//t2[0]
    t4 = cv.conversion_time(t_s)
    d4 = "{0}:{1}:{2}".format(t4[0],t4[1],t4[2])
    yd.append(d4)
    ##総残業時間取得
    sql4 ='select sum_time from zangyo where year = %s and month = %s order by id desc limit 1'
    cursor.execute(sql4,(y, m))
    gt = cursor.fetchone()
    t5 = cv.conversion_time(gt[0])
    d5 = "{0}:{1}:{2}".format(t5[0],t5[1],t5[2])
    yd.append(d5)
    #平均残業時間
    t6 = cv.conversion_time(gt[0]//t2[0])
    d6 = "{0}:{1}:{2}".format(t6[0],t6[1],t6[2])
    yd.append(d6)
    #残業時間対比
    t7 = cv.conversion_second(r_h, r_m, r_s)
    d7 = "{:.1%}".format(gt[0] / t7)
    yd.append(d7)
    return  yd

def graphing(y, m):
    #残業時間2時間超えた日の集計
    sql = 'select count(hour) from zangyo where year = %s and hour >= 2 group by month;'
    cursor.execute(sql, (y,))
    t1 = cursor.fetchall()
    count_list = []
    for c in t1:
        count_list.append(c[0])

    month_list = []
    m = 6
    while m >= 1:
        month_list.append(m)
        m -= 1
    else:
        month_list = sorted(month_list)
    #グラフ化してgraph.pngへ保存
    fig = plt.figure(figsize=(12, 8), dpi=72,
                     facecolor='skyblue', linewidth=10, edgecolor='green')
    ax = fig.add_subplot(111, xticklabels=month_list)
    ax.set_xlabel('Month')
    ax.set_ylabel('Count number')
    ax.set_title('Day over 2 hours List')
    ax.plot(count_list)
    fig.savefig('graph.png',facecolor=fig.get_facecolor(), edgecolor=fig.get_edgecolor())
    return count_list
