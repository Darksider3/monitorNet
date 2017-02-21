import datetime
import time

def timerStr(formatstrDate="[%d.%m.%y]", formatstrTime="[%H:%M:%S] -> "):
	return datetime.date.today().strftime(formatstrDate)+time.strftime(formatstrTime)

def fullStr(datetimestr, appendStr):
	return datetimestr+appendStr
