# ////////////////////////////////////////////////////////////////////////////////
# //
# //  WARECLOUD
# //
# ////////////////////////////////////////////////////////////////////////////////

import os
import time
import psutil
import threading
import subprocess
from Models.eprint import eprint

threads = []


class Installer:

    def __init__(self):
        self.name = ""
        self.path = "./install"

    def init(self, p_name):
        print("//////////////////\nInstaller: INITIALISATION\n//////////////////")
        self.name = p_name

    def install(self):
        installer = os.path.dirname(os.path.abspath(__file__)) + "\install\\" + self.name
        subprocess.call([installer])
        return

    def follower(self, name):
        statut = ""
        list_pid = psutil.pids()
        eprint("Installer: FOLLOWING PROCESS")
        for x in list_pid:
            if psutil.pid_exists(x) is True:
                p = psutil.Process(x)
                if p.name() == name:
                    eprint("Found!")
                    process = p
                    statut = process.status()
                    if str(statut) == "running":
                        return str(statut)
        return statut

# print(process.cpu_times())  # return cached value
# print(process.cpu_percent())  # return cached value
# print(process.create_time())  # return cached value
# print(process.ppid()) # return cached value



