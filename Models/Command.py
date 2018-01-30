
import platform
import os
from installer import *
from parse import *
import os
import time
import psutil
import threading

LINUX = "Linux"
WINDOWS = "Windows"

threads = []


class Command:

    """  Handles for received messages """
    def __init__(self, command):
        self.name = ""
        self.version = ""
        self.l_installer = Installer()

        self.parsed_command = str(command).split()

        self.m_Commands = dict()
        self.m_Commands["install"] = self.install
        self.m_Commands["follow"] = self.follow
        self.m_Commands["configure"] = self.download
        self.m_Commands["uninstall"] = self.download
        self.m_Commands["update"] = self.download
        self.m_Commands["download"] = self.download

    def is_valid_command(self):
        for l_command in self.m_Commands:
            if l_command == self.parsed_command[0]:
                if l_command == "install":
                    self.install(self.parsed_command[1], 0)
                if l_command == "follow":
                    self.follow()
                if l_command == "download":
                    self.download(self.parsed_command[1], self.parsed_command[2])
                #self.m_Commands[l_command](self.parsed_command[1], self.parsed_command[2])
                #print("#####COMMANDE TROUVER##### : " + l_command)
                return True

        return False

    def follow(self):
        print("NO")#self.l_installer.follower())

    def install(self, name, path):
        profile = ""
        if platform.system() == LINUX:
            os.system("apt-get update")
            os.system("apt-get --assume-yes install firefox")
            with open("/home/root/.mozilla/firefox/profiles.ini", "r+") as f:
                for line in f:
                    if line == 'Path=kt0pxqf3.default\n':
                        line = 'Path=xa6dylzk.clean\n'
                    profile += line
                f.seek(0)
                f.write(profile)
                f.truncate()
                f.close()

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

