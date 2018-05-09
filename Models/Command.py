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

from installer import *
from Models.Packet import *

LINUX = "Linux"
WINDOWS = "Windows"

threads = []
m_bool = False

ConfigurationPath = "%AppData%/"

Firefox = "Mozilla"
TeamViewer = "TeamViewer"
Slack = "Slack"
Chrome = "C:\\Users\\Cloquet Alban\\AppData\\Local\\Google\\Chrome\\User Data"


class Command:

    """  Handles for received messages """
    def __init__(self):
        self.name                       = ""
        self.version                    = ""
        self.l_installer                = Installer()
        self.parsed_command             = ""
        self.m_Commands                 = dict()
        self.m_Commands["install"]      = self.install
        self.m_Commands["follow"]       = self.follow
        self.m_Commands["configure"]    = self.download
        self.m_Commands["uninstall"]    = self.download
        self.m_Commands["update"]       = self.download
        self.m_Commands["download"]     = self.download


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
                return self.install(self.parsed_command[1], 0)
            if self.parsed_command[0] == "follow":
                return self.follow(self.parsed_command[1])
            if self.parsed_command[0] == "download":
                return self.download(self.parsed_command[1], self.parsed_command[2])
            if self.parsed_command[0] == "configure":
                return self.configure(self.parsed_command[1], self.parsed_command[2])

    """  Follow Process """
    def follow(self, name):
        packet = ""
        status = self.l_installer.follower(name)
        if status == "running":
            packet = PacketError(self.parsed_command[0], Enum.F_RUNNING)
        else:
            packet = PacketError(self.parsed_command[0], Enum.F_FINISH)
        packet.id = Enum.PACKET_FOLLOW
        return packet

    """  Configuration Software """
    def configure(self, name, path):
        return True

    """  Installation Software """
    def install(self, name, path):
        self.l_installer.init(name)
        t = threading.Thread(target=self.l_installer.install)
        threads.append(t)
        t.start()
        return PacketError(self.parsed_command[0], Enum.OK_INSTALL)

    """  Download Software """
    def download(self, url, file_name):
        import urllib.request
        # Download the file from `url` and save it locally under `file_name`:
        # https://stubdownloader.cdn.mozilla.net/builds/firefox-stub/fr/win/9705c66ad49acf77f0e875327f07d4ab65a4d7921dce9d41d6f421665a2b467b/Firefox%20Installer.exe
        return urllib.request.urlretrieve(url, "install/" + file_name)

