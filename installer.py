# ////////////////////////////////////////////////////////////////////////////////
# //
# //  WARECLOUD
# //
# ////////////////////////////////////////////////////////////////////////////////

import os
import time
import psutil
import threading


threads = []


class Installer:

    def __init__(self):
        self.name = ""
        self.path = "./install"

    def init(self, p_name):
        print("\n//////////////////\nInstaller: INITIALISATION\n//////////////////")
        self.name = p_name

    def install(self):
        os.system("C:\\" + self.name)
        return

    def follower(self):
        time.sleep(5)
        list_pid = psutil.pids()
        print("Installer: FOLLOWING PROCESS")
        for x in list_pid:
            if psutil.pid_exists(x) is True:
                p = psutil.Process(x)
                if p.name() == self.name + '.exe':
                    print("Found!")
                    process = p
        with process.oneshot():
           return process.name(), process.status()

# print(process.cpu_times())  # return cached value
# print(process.cpu_percent())  # return cached value
# print(process.create_time())  # return cached value
# print(process.ppid()) # return cached value



