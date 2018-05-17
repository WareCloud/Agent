#!/usr/bin/env python3
# title				: server.py
# description		: Simple implementation of server
# author			: Cloquet Alban
# date				: 2017/06/19
# version			: Python 3.6
# usage				: python server.py
# notes				:
# python_version	: 3.6
# ==============================================================================

# ////////////////////////////////////////////////////////////////////////////////
# //
# //  WARECLOUD
# //
# ////////////////////////////////////////////////////////////////////////////////

import sys
import threading
from urllib.request import urlretrieve

from Model.Packet import *

from Model.copytree import copytree

from installer import *

LINUX = "Linux"
WINDOWS = "Windows"

threads = []
m_bool = False

ConfigurationPath = "%AppData%/"


TeamViewer = "TeamViewer"
Slack = "Slack"

ConfigurationFolderChrome = "C:\\Users\\" + getpass.getuser() + "\\AppData\\Local\\"
Chrome = "Chrome"

Firefox = "Mozilla"
NotePad = "Notepad++"
ConfigurationFolder = "C:\\Users\\%s\\AppData\\Roaming\\" % (getpass.getuser())


GoogleChrome = "chrome.exe"


class Command:
    """  Handles for received messages """
    server = None
    client = None
    file_name = ""

    def __init__(self):
        self.name = ""
        self.version = ""
        self.file_name = ""
        self.l_installer = Installer()
        self.parsed_command = ""
        self.m_Commands = dict()
        self.m_Commands["install"] = self.install
        self.m_Commands["follow"] = self.follow
        self.m_Commands["configure"] = self.download
        self.m_Commands["uninstall"] = self.download
        self.m_Commands["update"] = self.download
        self.m_Commands["download"] = self.download

    def set_websocket(self, server, clients):
        Command.server = server
        Command.client = clients

    def new_command(self, command):
        self.parsed_command = str(command).split()

    """  Check if the Command is valid """
    def is_valid_command(self):
        for l_command in self.m_Commands:
            if l_command == self.parsed_command[0]:
                return True

        return False

    """  Execute Command """
    def run(self):
        if self.parsed_command[0] == "install":
            return self.install(self.parsed_command[1])
        if self.parsed_command[0] == "follow":
            return self.follow(self.parsed_command[1])
        if self.parsed_command[0] == "download":
            return self.download(self.parsed_command[1], self.parsed_command[2])
        if self.parsed_command[0] == "configure":
            return self.configure(self.parsed_command[1])

    """  Follow Process """
    def follow(self, name):
        status = self.l_installer.follower(name)
        if status == "running":
            packet = PacketError(self.parsed_command[0], PacketType.F_RUNNING, Enum.PACKET_FOLLOW)
        else:
            packet = PacketError(self.parsed_command[0], PacketType.F_FINISH, Enum.PACKET_FOLLOW)

        packet.path = name
        return packet

    """  Configuration Software """
    def configure(self, name):
        if name == NotePad:
            copytree('configuration\\' + NotePad, ConfigurationFolder + NotePad)
        if name == "Firefox":
            copytree('configuration\\' + Firefox, ConfigurationFolder + Firefox)
        if name == Chrome:
            copytree('configuration\\Google', ConfigurationFolderChrome)

        packet = PacketError(self.parsed_command[0], PacketType.OK_CONFIGURATION, Enum.PACKET_CONFIGURATION)
        packet.path = name + '.exe'
        return packet

    """  Installation Software """
    def install(self, name):
        self.l_installer.init(name)
        t = threading.Thread(target=self.l_installer.install, args=(Command.server, Command.client))
        threads.append(t)
        t.start()
        return

    """  Download Software """
    def download(self, url, file_name):
        Command.file_name = file_name
        threading.Thread(target=urlretrieve, args=(url, 'install/' + file_name, self.reporthook)).start()
        return

    @staticmethod
    def reporthook(blocknum, blocksize, totalsize):
        readsofar = blocknum * blocksize
        if totalsize > 0:
            percent = readsofar * 1e2 / totalsize
            packet = PacketError(percent, PacketType.F_RUNNING, Enum.PACKET_DOWNLOAD_STATE)
            packet.path = Command.file_name
            Command.server.send_message(Command.client, packet.toJSON())
            if readsofar >= totalsize:  # near the end
                sys.stderr.write("\n")
                packet = PacketError(percent, PacketType.F_FINISH, Enum.PACKET_DOWNLOAD_STATE)
                packet.path = Command.file_name
                Command.server.send_message(Command.client, packet.toJSON())
        else:  # total size is unknown
            sys.stderr.write("read %d\n" % (readsofar,))
