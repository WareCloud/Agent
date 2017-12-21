# ////////////////////////////////////////////////////////////////////////////////
# //
# //  WARECLOUD
# //
# ////////////////////////////////////////////////////////////////////////////////

import os
import time


import psutil
import threading


name = "FirefoxInstaller"
threads = []

class Installer:

    def __int__(self, p_name):
            self.name = p_name
            self.path = "./install"

    def install(self):
        os.system("C:\\" + name)
        return

    def follower(self):
        time.sleep(5)
        list_pid = psutil.pids()
        for x in list_pid:
            if psutil.pid_exists(x) is True:
                p = psutil.Process(x)
                if p.name() == self.name + '.exe':
                    print("Found!")
                    process = p
        with process.oneshot():
           print(process.name())  # execute internal routine once collecting multiple info
           print(process.cpu_times())  # return cached value
           print(process.cpu_percent())  # return cached value
           print(process.create_time())  # return cached value
           print(process.ppid()) # return cached value
           print(process.status())  # return cached value


l_installer = Installer("FirefoxInstaller")
t = threading.Thread(target=l_installer.installer)
threads.append(t)
t.start()
l_installer.follower()
print('finish')





