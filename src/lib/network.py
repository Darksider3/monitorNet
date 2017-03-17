import requests
import time
import os
import colors


class network:
    def __init__(self, host, httpTimeout=3, pingTimeout=1000, sleepTimer=10, httpExceptionTimer=2, defaultProt="https://"):
        self.httpTimeout = httpTimeout
        self.pingTimeout = pingTimeout
        self.sleepTimer = sleepTimer
        self.httpExceptionTimer = httpExceptionTimer
        self.host=host
        self.defaultProt=defaultProt
        self.__checkHost__()
        self.score = 0


    def __checkHost__(self):
        if "https://" not in self.host:
            if "http://" not in self.host:
                self.prot=self.defaultProt
                self.host = self.defaultProt + self.host
            else:
                self.prot="http://"
        else:
            self.prot="https://"


    def ping(self):
        # strip the protocol from the string
        self.host=self.host.replace(self.prot, '')
        # ping
        timeoutparam = "-w %s" % self.pingTimeout if colors.OS == "NT" else ""
        param = "-n 1" if colors.OS == "NT" else "-c 1"
        out = ">NUL" if colors.OS == "NT" else "2>&1 /dev/null"
        status=os.system("ping %s %s %s %s" % (timeoutparam, param, self.host, out)) == 0
        # revert changes
        self.host=self.prot+self.host

        return status


    def httpsUp(self):
        try:
            requests.get(self.host, verify=True, timeout=self.httpTimeout)
            return True
        except requests.exceptions.RequestException as e:
            time.sleep(self.httpExceptionTimer)
            return False


    def __scoreAdd__(self, num):
        self.score += num


    def __scoreSub__(self, num):
        self.score -= num
