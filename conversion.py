def conversion_time(d):
  hour = d // 3600
  hour_amari = d % 3600
  minute = hour_amari // 60
  second = hour_amari % 60
  if second >= 60:
    minute += 1
    second -= 60
  if minute >= 60:
    hour += 1
    minute -= 60
  return hour, minute, second

def conversion_sum(e,f,g):
  second = e % 60
  minute_sum = (f + (e // 60))
  minute = minute_sum % 60
  hour = g + (minute_sum // 60)
  if second >= 60:
    minute += 1
    second -= 60
  if minute >= 60:
    hour += 1
    minute -= 60
  return hour, minute, second

def conversion_second(h,i,j):
  second = (h * 3600) + (i * 60) + j
  return second