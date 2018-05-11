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
from Models.eprint import eprint
from urllib.request import urlretrieve
import sys

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
    server = None
    client = None

    def __init__(self):
        self.name = ""
        self.version = ""
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
            packet = PacketError(self.parsed_command[0], PacketType.F_RUNNING, Enum.PACKET_FOLLOW)
        else:
            packet = PacketError(self.parsed_command[0], PacketType.F_FINISH, Enum.PACKET_FOLLOW)
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
        return PacketError(self.parsed_command[0], PacketType.OK_INSTALL, Enum.PACKET_INSTALL)

    """  Download Software """
    def download(self, url, file_name):
        # Download the file from `url` and save it locally under `file_name`:
        # https://stubdownloader.cdn.mozilla.net/builds/firefox-stub/fr/win/9705c66ad49acf77f0e875327f07d4ab65a4d7921dce9d41d6f421665a2b467b/Firefox%20Installer.exe
        # urlretrieve(url, 'downloaded_file.py', self.reporthook)
        threading.Thread(target=urlretrieve, args=(url, 'downloaded_file.py', self.reporthook)).start()
        return

    @staticmethod
    def reporthook(blocknum, blocksize, totalsize):
        readsofar = blocknum * blocksize
        if totalsize > 0:
            percent = readsofar * 1e2 / totalsize
            s = "\r%5.1f%% %*d / %d" % (
                percent, len(str(totalsize)), readsofar, totalsize)
            sys.stderr.write(s)
            Command.server.send_message(Command.client, PacketError(s, PacketType.F_RUNNING, Enum.PACKET_DOWNLOAD_STATE).toJSON())
            if readsofar >= totalsize:  # near the end
                sys.stderr.write("\n")
                Command.server.send_message(Command.client, PacketError(s, PacketType.F_FINISH, Enum.PACKET_DOWNLOAD_STATE).toJSON())
        else:  # total size is unknown
            sys.stderr.write("read %d\n" % (readsofar,))
