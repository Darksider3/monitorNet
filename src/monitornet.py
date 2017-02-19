import requests
import time
import datetime
import subprocess #PING and so one, heh?
#custom shit tho
import colors

#sqlite for database purposes

import sqlite3 as lite
import sys
import os

def sqliteCleanOldEntrys(handle, expireVal, month=False):
	if month==False:
		expireParam="day"
	else:
		expireParam="month"
	with handle:
		cur=con.cursor()
		cur.execute("DELETE FROM down WHERE Timestamp <= date('now', '-%s %s')"%(expireVal, expireParam))

def sqliteCleanDB(handle):
	with handle:
		cur=con.cursor()
		cur.execute("DROP TABLE IF EXISTS down")


def __ping(host, timeout=100):
    timeoutparam=""
    param="-n 1" if colors.OS == "NT" else "-c 1"
    out=">NUL" if colors.OS == "NT" else "2>&1 /dev/null"
    return os.system("ping %s %s >NUL"%(param, host))==0

	
# if __ping("fuckallthedayasdasdasdaskdlahsd-muuuh.com"):
# 	print "yes"
# else: 
# 	print "nop"
def isitup(host, defaultProt="https://", timeoutT=3, Ping=False, PingTimeout=100):
	# if __ping(host, PingTimeout)==False:
	# 	return False
    if "https://" not in host:
        if "http://" not in host:
            host=defaultProt+host
    try:
        r=requests.get(host, verify=True, timeout=timeoutT)
        return True
    
    except requests.exceptions.RequestException as e:
        time.sleep(httpExceptionSleep)
        return False;

DATABASE = "down.db"
try:
	con=lite.connect(DATABASE)
except:
	pass
finally:
	con.close()
	con=lite.connect(DATABASE)

with con:
     cur=con.cursor()
     cur.execute("CREATE TABLE IF NOT EXISTS down(" \
				 "id INTEGER PRIMARY KEY," \
				 "Timestamp INTEGER(4) DEFAULT CURRENT_TIMESTAMP," \
				 "url TEXT," \
				 "timeoutTime INTEGER," \
				 "up BOOL DEFAULT FALSE" \
				 ")")

sqliteCleanOldEntrys(con, 1, month=True)


#constants
TESTLIST=["lasdf", "localbreak", "google.com", "google.de"]
hostList=["google.de", "google.com", "http://darksider3.de/", "duckduckgo.com"]
ListLength=3

# Timer configs
httpTimeout=2 # Timeout for HTTP/S
pingTimeout=3 # Milliseconds
sleepTimer=10 # Sleep for X seconds if it actually works to ping again
httpExceptionSleep=3 # Seconds


#Variable content
i=0
timestr=""


while False!=True:
	while isitup(hostList[i], timeoutT=httpTimeout)==False:
		"""
		Handle false positives
		The if-clause if simply to don't go out of range of i. Checking on NULL or against an exception Object isn't good^^
		"""
		if isitup(hostList[i +1 if i!=ListLength else i-1], timeoutT=httpTimeout)==True:
			if i == ListLength:
				i=0
			else:
				i+=1
			break
		timestr=datetime.date.today().strftime("[%d.%m.%y]")+time.strftime("[%H:%M:%S] -> ") #get it again every rotation
		colors.printer("[!!!] DOWN [!!!] URL: %s"%hostList[i], timestr, down=True)
		# now put it into the db
		with con:
			cur=con.cursor()
			insertstr="INSERT INTO down(url, timeoutTime) VALUES('%s', '%i')"%(hostList[i], httpTimeout)
			cur.execute(insertstr)
        if i==ListLength:
            i=0
        else:
            i+=1


	with con:
		cur=con.cursor()
		insertstr="INSERT INTO down(url, up) VALUES('%s', 'True')"%hostList[i]
		#print insertstr
		cur.execute(insertstr)
	"""
	get it again every rotation
	"""
	timestr=datetime.date.today().strftime("[%d.%m.%y]")+time.strftime("[%H:%M:%S] -> ")
	colors.printer("[!] UP [!] URL: %s"%hostList[i], timestr, down=False)

	"""
	sleep specific amount of time to don't spam traffic(obvious, if you think about it, heh?)
	
	The exceptions here are used because we can't close or interact with the SQLite DB anymore, and if something happens(SIG_EXIT, heh?)
	we need to exit properly, including close the database.
	"""
	try:
		if i == ListLength:
			i=0
		else:
			i+=1
		time.sleep(sleepTimer)
	except:
		con.close()
		sys.exit(1)

with con:
	con.close()

colors.printer("Roger Roger guys, we're backs UP", timestr, down=False)