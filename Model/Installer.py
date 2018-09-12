# ////////////////////////////////////////////////////////////////////////////////
# //
# //  WARECLOUD
# //
# ////////////////////////////////////////////////////////////////////////////////

import subprocess
import psutil
from Model.Packet import *
from Model.Logger import *
from Model.SoftwareInfo import *


class Installer:

    def __init__(self):
        self.software = ""
        self.path = "./install"

    def init(self, p_name):
        Logger.__call__().get_logger().info("Installer: INITIALISATION")
        self.software = p_name

    def install(self, server, client):
        installer = "install\\" + self.software.file
        try:
            if self.software.file == "Chrome.exe":
                subprocess.check_call(installer + " /silent /install", shell=True)
            else:
                subprocess.check_call(installer + " /S", shell=True)
        except subprocess.CalledProcessError as e:
            Logger.__call__().get_logger().debug(e)
            server.send_message(client, PacketError(self.software.file, PacketType.FAILED_INSTALL, Enum.PACKET_INSTALL, self.software.name).toJSON())
            return  # handle errors in the called executable
        except OSError as e:
            Logger.__call__().get_logger().debug(e.filename + " " + e.errno + " " + e.strerror)
            server.send_message(client, PacketError(self.software.file, PacketType.FAILED_FIND_INSTALLER, Enum.PACKET_INSTALL, self.software.name).toJSON())
            return # executable not found

        server.send_message(client, PacketError(self.software.file, PacketType.OK_INSTALL, Enum.PACKET_INSTALL, self.software.name).toJSON())
        return True

    def uninstall(self, server, client):
        softwareInfo = SoftwareInfo()
        softwares = softwareInfo.get_all_software()
        call = ''

        for x in softwares.arraySoft:
            if x.name.find(self.software.file) != -1:
                call = x.uninstall
        try:
            subprocess.check_call(call, shell=True)
        except subprocess.CalledProcessError as e:
            Logger.__call__().get_logger().debug(e)
            server.send_message(client, PacketError(self.software.file,
                                                    PacketType.FAILED_UNINSTALL, Enum.PACKET_UNINSTALL, self.software.name).toJSON())
            return  # handle errors in the called executable
        except OSError as e:
            Logger.__call__().get_logger().debug(e.filename + " " + e.errno + " " + e.strerror)
            server.send_message(client,
            PacketError(self.software.file,
                        PacketType.FAILED_FIND_UNINSTALLER, Enum.PACKET_UNINSTALL, self.software.name).toJSON())
            return  # executable not found

        server.send_message(client, PacketError(self.software.file,
                                                PacketType.OK_UNINSTALL, Enum.PACKET_UNINSTALL, self.software.name).toJSON())
        return True

    def follower(self, name):
        statut = ""
        list_pid = psutil.pids()
        Logger.__call__().get_logger().info("Installer: FOLLOWING PROCESS")
        for x in list_pid:
            if psutil.pid_exists(x) is True:
                p = psutil.Process(x)
                if p.name():
                    eprint(p.name())

                eprint("statut follow : " + statut)
                if p.name() == name:
                    eprint("Found!")
                    process = p
                    statut = process.status()
                    if str(statut) == "running":
                        return str(statut)

        eprint("statut follow : " + statut)
        return statut



