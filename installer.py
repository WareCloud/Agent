# ////////////////////////////////////////////////////////////////////////////////
# //
# //  WARECLOUD
# //
# ////////////////////////////////////////////////////////////////////////////////

import subprocess
import psutil
from Model.Packet import *
from Model.Logger import *

threads = []


class Installer:

    def __init__(self):
        self.name = ""
        self.path = "./install"

    def init(self, p_name):
        Logger.__call__().get_logger().info("Installer: INITIALISATION")
        self.name = p_name

    def install(self, server, client):
        installer = "install\\" + self.name
        print(installer)
        try:
            if self.name == "Chrome.exe":
                subprocess.check_call(installer + " /silent /install", shell=True)
            else:
                subprocess.check_call(installer + " /S", shell=True)
        except subprocess.CalledProcessError as e:
            Logger.__call__().get_logger().debug(e)
            server.send_message(client, PacketError(self.name, PacketType.FAILED_INSTALL, Enum.PACKET_INSTALL).toJSON())
            return  # handle errors in the called executable
        except OSError as e:
            Logger.__call__().get_logger().debug(e.filename + " " + e.errno + " " + e.strerror)
            server.send_message(client, PacketError(self.name, PacketType.FAILED_FIND_INSTALLER, Enum.PACKET_INSTALL).toJSON())
            return # executable not found

        print(PacketError(self.name, PacketType.OK_INSTALL, Enum.PACKET_INSTALL).toJSON())
        server.send_message(client, PacketError(self.name, PacketType.OK_INSTALL, Enum.PACKET_INSTALL).toJSON())
        return True

    def follower(self, name):
        statut = ""
        list_pid = psutil.pids()
        Logger.__call__().get_logger().info("Installer: FOLLOWING PROCESS")
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



