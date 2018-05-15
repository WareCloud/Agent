# ////////////////////////////////////////////////////////////////////////////////
# //
# //  WARECLOUD
# //
# ////////////////////////////////////////////////////////////////////////////////

import os
import subprocess

import psutil
from Model.Packet import *

from Model.eprint import eprint

threads = []


class Installer:

    def __init__(self):
        self.name = ""
        self.path = "./install"

    def init(self, p_name):
        print("//////////////////\nInstaller: INITIALISATION\n//////////////////")
        self.name = p_name

    def install(self, server, client):
        installer = "install\\" + self.name
        print(installer)
        try:
            subprocess.check_call(installer + " /S", shell=True)
        except subprocess.CalledProcessError:
            server.send_message(client, PacketError(self.name, PacketType.FAILED_INSTALL, Enum.PACKET_INSTALL).toJSON())
            return  # handle errors in the called executable
        except OSError:
            server.send_message(client, PacketError(self.name, PacketType.FAILED_FIND_INSTALLER, Enum.PACKET_INSTALL).toJSON())
            return # executable not found

        print(PacketError(self.name, PacketType.OK_INSTALL, Enum.PACKET_INSTALL).toJSON())
        server.send_message(client, PacketError(self.name, PacketType.OK_INSTALL, Enum.PACKET_INSTALL).toJSON())
        return True

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



