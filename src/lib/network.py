import requests
import time
import os
import lib.colors as colors


class network:
    def __init__(self, hostList, hostListLength, httpTimeout=3, pingTimeout=1000, sleepTimer=10, httpExceptionTimer=2):
        self.httpTimeout = httpTimeout
        self.pingTimeout = pingTimeout
        self.sleepTimer = sleepTimer
        self.httpExceptionTimer = httpExceptionTimer
        self.hostList = hostList
        self.hostSize = hostListLength
        self.__checkHostList__()
        self.score = 0

    def __checkHostList__(self):
        pass  # @todo: check host list for http/https

    def __ping__(self, hostnr):
        timeoutparam = "-w %s" % self.pingTimeout if colors.OS == "NT" else ""
        param = "-n 1" if colors.OS == "NT" else "-c 1"
        out = ">NUL" if colors.OS == "NT" else "2>&1 /dev/null"
        return os.system("ping %s %s %s %s" % (timeoutparam, param, self.hostList[hostnr], out)) == 0

    def httpsUp(self, hostnr):
        try:
            r = requests.get(self.hostList[hostnr], verify=True, timeout=self.httpTimeout)
            return True
        except requests.exceptions.RequestException as e:
            time.sleep(self.httpExceptionTimer)
            return False

    def __scoreAdd__(self, num):
        self.score += num

    def __scoreSub__(self, num):
        self.score -= num
