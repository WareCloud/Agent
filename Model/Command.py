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
ConfigurationFolder = "C:\\Users\\%s\\AppData\\Roaming\\" % (getpass.getuser())

class Command:
    """  Handles for received messages """
    server = None
    client = None
    fileName = ""
    timer = 0

    def __init__(self):
        self.logger = Logger.__call__().get_logger()
        self.version = ""
        self.file_name = ""
        self.l_installer = Installer()
        self.parsed_command = ""
        self.m_Commands = dict()
        self.m_Commands["install"] = self.install
        self.m_Commands["follow"] = self.follow
        self.m_Commands["ping"] = self.ping
        self.m_Commands["configure"] = self.configure
        self.m_Commands["uninstall"] = self.uninstall
        self.m_Commands["update"] = self.download
        self.m_Commands["download"] = self.download
        self.m_Commands["download_cfg"] = self.download_cfg

    """ Init Websocket in the classe"""
    def set_websocket(self, server, clients):
        Command.server = server
        Command.client = clients

    """ Parsing Commands """
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

    def new_command(self, command):
        try:
            self.parsed_command = json.loads(command, object_hook=lambda d: namedtuple('X', d.keys())(*d.values()))
        except json.JSONDecodeError as e:
                eprintlog(format(str(e)))
                self.logger.debug(format(str(e)))
        else:
            self.logger.info(self.parsed_command)

    """  Check if the Command is valid """
    def is_valid_command(self):
        if hasattr(self.parsed_command, 'command'):
            for l_command in self.m_Commands:
                if l_command == self.parsed_command.command:
                    return True

        return False

    """  Execute Command """
    def run(self):
        return self.m_Commands[self.parsed_command.command]()

    """ Ping """
    def ping(self):
        return PacketError(self.parsed_command.command, PacketType.PING, Enum.PACKET_PING)

    """  Follow Process """
    def follow(self):
        status = self.l_installer.follower(self.parsed_command.software.file)
        if status == "running":
            packet = PacketError(self.parsed_command.software.file, PacketType.F_RUNNING, Enum.PACKET_FOLLOW, self.parsed_command.software.name)
        else:
            packet = PacketError(self.parsed_command.software.file, PacketType.F_FINISH, Enum.PACKET_FOLLOW, self.parsed_command.software.name)

        packet.path = self.parsed_command.software.path
        return packet

    """  Configuration Software """
    def configure(self):
        if self.parsed_command.software.extension == "tar.gz" or self.parsed_command.software.extension == "tgz":
            tar = tarfile.open('configuration\\' + self.parsed_command.software.file, "r:gz")
            tar.extractall('configuration\\' + self.parsed_command.software.name)
            tar.close()
            copytree('configuration\\' + self.parsed_command.software.name, ConfigurationFolder + self.parsed_command.software.path)

        packet = PacketError(self.parsed_command.software.file, PacketType.OK_CONFIGURATION, Enum.PACKET_CONFIGURATION, self.parsed_command.software.name)
        packet.path = self.parsed_command.software.path
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
            self.logger.debug(format(str(e)))
            packet = PacketError(e.code, PacketType.FAILED_DOWNLOAD, Enum.PACKET_DOWNLOAD_STATE, self.parsed_command.software.name)
            packet.path = self.parsed_command.software.path
            Command.server.send_message(Command.client, packet.toJSON())
        except URLError as urlerror:
            if hasattr(urlerror, 'reason'):
                self.logger.debug(format(str(e)))
                eprintlog('We failed to reach a server.')
                eprintlog('Reason: ', urlerror.reason)
                packet = PacketError(urlerror.reason, PacketType.FAILED_DOWNLOAD, Enum.PACKET_DOWNLOAD_STATE, self.parsed_command.software.name)
                packet.path = self.parsed_command.software.path
                Command.server.send_message(Command.client, packet.toJSON())
            elif hasattr(urlerror, 'code'):
                self.logger.debug(format(str(e)))
                eprintlog('The server couldn\'t fulfill the request.')
                eprintlog('Error code: ', urlerror.code)
                packet = PacketError(urlerror.code, PacketType.FAILED_DOWNLOAD, Enum.PACKET_DOWNLOAD_STATE, self.parsed_command.software.name)
                packet.path = self.parsed_command.software.path
                Command.server.send_message(Command.client, packet.toJSON())
        else:
            threading.Thread(target=urlretrieve, args=(self.parsed_command.software.url, 'install/' + self.parsed_command.software.file, self.reporthook)).start()
        return

    """  Download Configure """
    def download_cfg(self):
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
                                                       'configuration/' + self.parsed_command.software.file, self.reporthook_cfg)).start()
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
