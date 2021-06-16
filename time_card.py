from flask import Flask,render_template
import mysql.connector
import datetime
import time_record as tr
import db_config as dc
import db_write as dw
import db_analysis as da

app = Flask(__name__)

#トップページ表示
@app.route("/")
def index():
  message = tr.now_record()
  result = tr.attendance_list()
  result2 = tr.working_sum()
  result3 = tr.oversum_calc()
  return render_template('index.html',message = message, result = result, result2 = result2, result3 = result3)

#出勤時挙動
@app.route("/syusya")
def punch_in():
  message = "Good morning！"
  message2 = "Let's do our best today！"
  result = tr.stamping_in()
  return render_template('kintai.html',message = message, message2 = message2, result = result)

#退勤時挙動
@app.route("/taisya")
def punch_out():
  message = "Thank you for your hard work！"
  message2 = "Please rest at ease！"
  result = tr.stamping_out()
  result2 = tr.overtime_calc()
  return render_template('kintai.html',message = message,message2 = message2, result = result, result2 = result2)

#ファイル出力挙動
@app.route("/output")
def data_writing():
  message = "Output to CSV file has completed！"
  nr = tr.now_record()
  year = nr[2]
  month = nr[3]
  dw.data_write(year, month)
  return render_template('kintai.html', message = message)

#データ分析挙動
@app.route("/analysis")
def data_analysing():
  message = "Data analysis results"
  nr = tr.now_record()
  year = nr[2]
  month = nr[3]
  result_t = da.conv_yearday(year, month)
  result_1 = da.conv_yearday(year, month-1)
  result_2 = da.conv_yearday(year, month-2)
  result_3 = da.conv_yearday(year, month-3)
  result_4 = da.conv_yearday(year, month-4)
  result_5 = da.conv_yearday(year, month-5)
  return render_template('kaiseki.html', message = message, result_t = result_t, result_1 = result_1, result_2 = result_2, result_3 = result_3, result_4 = result_4, result_5 = result_5)

@app.route("/analysis/graph")
def data_graph():
  nr = tr.now_record()
  year = nr[2]
  month = nr[3]
  da.graphing(year, month)
  message = "Saved to graph is complete!!"
  return render_template('graph_show.html', message = message)

if __name__ == '__main__':
   #app.run(host="127.0.0.1", port=5000, debug=True)
    app.run(host="0.0.0.0", port=80, debug=False)