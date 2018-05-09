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

import threading

from Models.installer import *

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


    def is_valid_command(self):
        for l_command in self.m_Commands:
            if l_command == self.parsed_command[0]:
                return True

        return False

    def run(self):
            if self.parsed_command[0] == "install":
                self.install(self.parsed_command[1], 0)
            if self.parsed_command[0] == "follow":
                self.l_installer.follower(self.parsed_command[1])
            if self.parsed_command[0] == "download":
                self.download(self.parsed_command[1], self.parsed_command[2])
            if self.parsed_command[0] == "configure":
                self.configure(self.parsed_command[1], self.parsed_command[2])

    def follow(self, name):
        name, status = self.l_installer.follower(name)
        print(name, status)
        return status == "running"

    def configure(self, name, path):

        return True

    def install(self, name, path):
        print(name)
        self.l_installer.init(name)
        t = threading.Thread(target=self.l_installer.install)
        threads.append(t)
        t.start()
        return True

    def download(self, url, file_name):
        import urllib.request
        # Download the file from `url` and save it locally under `file_name`:
        # https://stubdownloader.cdn.mozilla.net/builds/firefox-stub/fr/win/9705c66ad49acf77f0e875327f07d4ab65a4d7921dce9d41d6f421665a2b467b/Firefox%20Installer.exe
        return urllib.request.urlretrieve(url, "install/" + file_name)

