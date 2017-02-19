import sys
import time
import logging
import os
import signal
import subprocess
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler
from watchdog.events import FileSystemEventHandler

class reRun(FileSystemEventHandler):
    def __init__(self, File, P): # subprocess.pid==PID
        self.proc=P
        self.File=File
    def on_modified(self, event):
        self.proc.kill()
        temp=subprocess.Popen(self.File, shell=False)
        self.proc=temp
        print("Killed and Respawn")
        
if __name__ == "__main__":
    temp= subprocess.Popen("python src/monitornet.py", shell=False)
    path = sys.argv[1] if len(sys.argv) > 1 else './src'
    event_handler = reRun("python src/monitornet.py", temp)
    observer = Observer()
    observer.schedule(event_handler, path)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()