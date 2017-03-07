import Queue as queue
from network import network

class URLJob:
    def __init__(self, url, priority, description=False, timeout=1):
        self.description=description
        self.priority=priority
        self.url=url
        self.timeout=timeout
        self.__task__()

    def __task__(self):
        pass

    def __cmp__(self, other):
        if not isinstance(other, Job):
            return None
        return cmp(self.priority, other.priority)


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
        if netobj.ping():
            self.ping=True
        else:
            self.ping=False

q=queue.Queue()
q.put(PingJob("darksider3.de", 1, "Test1", timeout=1000))
q.put(PingJob("google.de", 2, "googlede", timeout=1000))
q.put(PingJob("google.com", 3, "googlecom", timeout=1000))
q.put(PingJob("https://home.cern", 4, "cern", timeout=1000))
test=PingJob("example.com", 5, "example", timeout=1000)
print(test.ping)
print("Testing queue")
while not q.empty():
    next_job = q.get()
    print 'Processing PingJob:', next_job.description
    print('Result: '+str(next_job.ping))