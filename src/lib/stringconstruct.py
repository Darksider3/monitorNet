import datetime
import time


def timerstring(formatstringdate="[%d.%m.%y]", formatstringtime="[%H:%M:%S] -> "):
    return datetime.date.today().strftime(formatstringdate) + time.strftime(formatstringtime)


def fullstring(datetimestring, appendstring):
    return datetimestring + appendstring
