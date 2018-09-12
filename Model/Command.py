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
import tarfile
import threading
from urllib.request import urlretrieve
from urllib.error import URLError
import urllib

from django.core.exceptions import ImproperlyConfigured

from Model.copytree import copytree
from Model.Installer import *
import time
import json
from collections import namedtuple

LINUX = "Linux"
WINDOWS = "Windows"

threads = []
m_bool = False
ConfigurationPath = "%AppData%/"

TeamViewer = "TeamViewer"
Slack = "Slack"
Firefox = "Mozilla"
NotePad = "Notepad++"
ConfigurationFolder = "C:\\Users\\%s\\AppData\\Roaming\\" % (getpass.getuser())

#Chrome = "Chrome"
#ConfigurationFolderChrome = "C:\\Users\\" + getpass.getuser() + "\\AppData\\Local\\"
#GoogleChrome = "chrome.exe"

class Command:
    """  Handles for received messages """
    server = None
    client = None
    fileName = ""
    timer = 0

    def __init__(self):
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
        self.m_Commands["download_cfg"] = self.download_cfg

    """ Init Websocket in the classe"""
    def set_websocket(self, server, clients):
        Command.server = server
        Command.client = clients

    """ Parsing Commands """
    def new_command(self, command):
        try:
            self.parsed_command = json.loads(command, object_hook=lambda d: namedtuple('X', d.keys())(*d.values()))
        except json.JSONDecodeError as e:
                eprintlog(format(str(e)))
        else:
            eprintlog(self.parsed_command)


    """  Check if the Command is valid """
    def is_valid_command(self):
        if hasattr(self.parsed_command, 'command'):
            for l_command in self.m_Commands:
                if l_command == self.parsed_command.command:
                    return True

        return False

    """  Execute Command """
    """             Name            [Commande]         [link]           [File_register] """
    """  Example:   Mozilla          install        path/to/mozilla/       Firefox.exe """
    def run(self):
        return self.m_Commands[self.parsed_command.command]()


    """  Follow Process """
    def follow(self):
        status = self.l_installer.follower(self.parsed_command.software.file)
        if status == "running":
            packet = PacketError(self.parsed_command.command, PacketType.F_RUNNING, Enum.PACKET_FOLLOW, self.parsed_command.name)
        else:
            packet = PacketError(self.parsed_command.command, PacketType.F_FINISH, Enum.PACKET_FOLLOW, self.parsed_command.name)
        packet.path = self.software.path
        return packet

    """  Configuration Software """
    def configure(self):

        import tarfile
        if self.parsed_command.software.file.endswith("tar.gz"):
            tar = tarfile.open(name, "r:gz")
            tar.extractall()
            tar.close()
            copytree('configuration\\' + name, ConfigurationFolder + name)

        #Chrome is now removed
        #if name == Chrome:
        #    copytree('configuration\\Google', ConfigurationFolderChrome)

        packet = PacketError(self.parsed_command.command, PacketType.OK_CONFIGURATION, Enum.PACKET_CONFIGURATION)
        packet.path = self.parsed_command.software.name
        return packet

    """  Installation Software """
    def install(self):
        self.l_installer.init(self.parsed_command.software)
        t = threading.Thread(target=self.l_installer.install, args=(Command.server, Command.client))
        threads.append(t)
        t.start()
        return

    """  Uninstallation Software """
    def uninstall(self):
        self.l_installer.init(self.parsed_command.software)
        t = threading.Thread(target=self.l_installer.uninstall, args=(Command.server, Command.client))
        threads.append(t)
        t.start()
        return

    """  Download Software """
    def download(self):
        self.fileName = self.parsed_command.software.file
        try:
            urllib.request.urlopen(self.parsed_command.software.url)
        except urllib.error.HTTPError as e:
            eprintlog(e.code)
            eprintlog(e.read())
            packet = PacketError(e.code, PacketType.FAILED_DOWNLOAD, Enum.PACKET_DOWNLOAD_STATE, self.parsed_command.software.name)
            packet.path = self.parsed_command.software.path
            Command.server.send_message(Command.client, packet.toJSON())
        except URLError as urlerror:
            if hasattr(urlerror, 'reason'):
                eprintlog('We failed to reach a server.')
                eprintlog('Reason: ', urlerror.reason)
                packet = PacketError(urlerror.reason, PacketType.FAILED_DOWNLOAD, Enum.PACKET_DOWNLOAD_STATE, self.parsed_command.software.name)
                packet.path = self.parsed_command.software.path
                Command.server.send_message(Command.client, packet.toJSON())
            elif hasattr(urlerror, 'code'):
                eprintlog('The server couldn\'t fulfill the request.')
                eprintlog('Error code: ', urlerror.code)
                packet = PacketError(urlerror.code, PacketType.FAILED_DOWNLOAD, Enum.PACKET_DOWNLOAD_STATE, self.parsed_command.software.name)
                packet.path = self.parsed_command.software.path
                Command.server.send_message(Command.client, packet.toJSON())
        else:
            threading.Thread(target=urlretrieve, args=(self.parsed_command.software.url, 'install/' + self.parsed_command.software.file, self.reporthook)).start()
        return

    """  Download Configure """
    """{
    {
     "command": "download_cfg",
     "software": {
       "name": "Firefox",
       "file": "Firefox.exe",
       "path": "AppData/Mozilla/Firefox",
       "url": "https://url/download/cfg"
       "extension": "tgz"
     }
    }
    """
    def download_cfg(self):
        try:
            urllib.request.urlopen(self.parsed_command.software.url)


        except urllib.error.HTTPError as e:
            eprintlog(e.code)
            eprintlog(e.read())
            packet = PacketError(e.code, PacketType.FAILED_DOWNLOAD, Enum.PACKET_DOWNLOAD_STATE, self.parsed_command.software.name)
            packet.path = self.parsed_command.software.path
            Command.server.send_message(Command.client, packet.toJSON())


        except URLError as urlerror:
            if hasattr(urlerror, 'reason'):
                eprintlog('We failed to reach a server.')
                eprintlog('Reason: ', urlerror.reason)
                packet = PacketError(urlerror.reason, PacketType.FAILED_DOWNLOAD, Enum.PACKET_DOWNLOAD_STATE_CFG, self.parsed_command.software.name)
                packet.path = self.parsed_command.software.url
                Command.server.send_message(Command.client, packet.toJSON())
            elif hasattr(urlerror, 'code'):
                eprintlog('The server couldn\'t fulfill the request.')
                eprintlog('Error code: ', urlerror.code)
                packet = PacketError(urlerror.code, PacketType.FAILED_DOWNLOAD, Enum.PACKET_DOWNLOAD_STATE_CFG, self.parsed_command.software.name)
                packet.path = self.parsed_command.software.url
                Command.server.send_message(Command.client, packet.toJSON())


        else:
            threading.Thread(target=urlretrieve, args=(self.parsed_command.software.url,
                                                       'configuration/' + self.parsed_command.software.name + self.parsed_command.software.extension, self.reporthook_cfg)).start()
        return

    def reporthook(self, blocknum, blocksize, totalsize):
        readsofar = blocknum * blocksize
        if totalsize > 0:
            percent = readsofar * 1e2 / totalsize
            currenttimer = int(round(time.time() * 1000))
            if currenttimer > self.timer + 500:
                self.timer = currenttimer
                packet = PacketError(percent, PacketType.F_RUNNING, Enum.PACKET_DOWNLOAD_STATE, self.parsed_command.software.name)
                packet.path = self.parsed_command.software.path
                Command.server.send_message(Command.client, packet.toJSON())

            if readsofar >= totalsize:  # near the end
                packet = PacketError(percent, PacketType.F_FINISH, Enum.PACKET_DOWNLOAD_STATE, self.parsed_command.software.name)
                packet.path = self.parsed_command.software.path
                Command.server.send_message(Command.client, packet.toJSON())
        else:  # total size is unknown
            sys.stderr.write("read %d\n" % (readsofar,))

    def reporthook_cfg(self, blocknum, blocksize, totalsize):
        readsofar = blocknum * blocksize
        if totalsize > 0:
            percent = readsofar * 1e2 / totalsize
            currenttimer = int(round(time.time() * 1000))
            if currenttimer > self.timer + 500:
                self.timer = currenttimer
                packet = PacketError(percent, PacketType.F_RUNNING, Enum.PACKET_DOWNLOAD_STATE_CFG, self.parsed_command.software.name)
                packet.path = self.parsed_command.software.path
                Command.server.send_message(Command.client, packet.toJSON())

            if readsofar >= totalsize:  # near the end
                packet = PacketError(percent, PacketType.F_FINISH, Enum.PACKET_DOWNLOAD_STATE_CFG, self.parsed_command.software.name)
                packet.path = self.parsed_command.software.path
                Command.server.send_message(Command.client, packet.toJSON())
        else:  # total size is unknown
            sys.stderr.write("read %d\n" % (readsofar,))
