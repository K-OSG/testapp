window.onload = function(){
  setInterval("showNowDate()", 1000);
}

function showNowDate(){
var nowTime = new Date(); //  現在日時を得る
var nowHour = nowTime.getHours(); // 時を抜き出す
var nowMin  = nowTime.getMinutes(); // 分を抜き出す
var nowSec  = nowTime.getSeconds(); // 秒を抜き出す
var msg = nowHour + " : " + nowMin + " : " + nowSec;
document.getElementById("RealtimeClockArea").innerHTML = msg;}