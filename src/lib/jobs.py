import queue
from network import network
import sqlite3 as lite


class URLJob:
    def __init__(self, url, priority, description=False, timeout=1):
        self.description=description
        self.priority=priority
        self.url=url
        self.timeout=self.timeout(timeout=timeout)
        self.__task__()

    def timeout(self, timeout=1):
        self.timeout=timeout
        return self.timeout

    def __task__(self):
        pass

    # def __cmp__(self, other):
    #     if not isinstance(other, URLJob):
    #         return None
    #     return cmp(self.priority, other.priority)

    def __lt__(self, other):
        if not isinstance(other, URLJob):
            return None
        return self.priority < other.priority


class HTTPSJob(URLJob):
    def __init__(self, url, priority, description, httptimeout=2, pingtimeout=1000, sleep=10, httpExceptionSleep=2, ping=True, exitonping=True):
        self.url=url
        self.description=description
        self.priority=priority
        netobj=network(self.url, httpTimeout=httptimeout, pingTimeout=pingtimeout, sleepTimer=sleep, httpExceptionTimer=httpExceptionSleep)
        if ping:
            if not netobj.ping():
                self.ping=False
                if exitonping:
                    return
            else:
                self.ping=True


class PingJob(URLJob):
    def __task__(self):
        netobj=network(self.url, pingTimeout=self.timeout)
        self.ping=netobj.ping() # gives True or False

    def timeout(self, timeout=1):
        self.timeout=timeout*1000
        return self.timeout


class SQLJob:
    def __init__(self, db="down.db"):
        self.db=db
        try:
            self.con=lite.connect(self.db)
        except:
            self.con.close()
            self.con=lite.connect(self.db)

    def __write__(self, query):
        with self.con:
            cur=self.con.cursor()
            return cur.execute(query)



q=queue.PriorityQueue()
q.put(PingJob("darksider3.de", 1, "Test1", timeout=1))
q.put(PingJob("google.de", 2, "googlede", timeout=1))
q.put(PingJob("google.com", 3, "googlecom", timeout=1))
q.put(PingJob("https://home.cern", 4, "cern", timeout=1))
test=PingJob("example.com", 5, "example", timeout=1)
print(test.ping)
print("Testing queue")
while not q.empty():
    next_job = q.get()
    print('Processing PingJob:', next_job.description)
    print('Result: '+str(next_job.ping))
