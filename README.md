# About

MonitorNet monitors the internet connection of the machine it is running on.
It simply tries to determinate the status of the connection with, at the moment, `ping` and HTTP/S requests
to high available services like google.*

# Install

It uses Python 3, requests and SQLite3, as well as the internal OS representation of `ping`

```
git clone https://github.com/Darksider3/monitorNet
cd monitorNet/src
python ./monitornet.py
```

It also has a Watchdog for changes in the project Python files(monitornet.py, colors.py). It uses watchdog:
```
cd monitorNet
python ./changeserv.py
```