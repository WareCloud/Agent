
import platform
import os
from parse import *

LINUX = "Linux"
WINDOWS = "Windows"

class Command:

    """  Handles for received messages """
    def __init__(self, command):
        self.name = ""
        self.version = ""
        self.m_command = str(command).split()
        self.m_Commands = dict()
        self.m_Commands["install"] = self.install
        self.m_Commands["configure"] = self.install
        self.m_Commands["uninstall"] = self.install
        self.m_Commands["update"] = self.install
        self.m_Commands["download"] = self.download

    def is_valid_command(self):
        for l_command in self.m_Commands:
            if l_command == self.m_command[0]:
                print(self.m_Commands)
                return self.m_Commands[l_command](self.m_command[1], self.m_command[2])

        return False

    def install(self):
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

        elif platform.system() == WINDOWS:
            os.system("C:\\Users\\cloqu\\Downloads\\Firefox.exe /S")
            with open("C:\\Users\\cloqu\\AppData\\Roaming\\Mozilla\\Firefox\\profiles.ini", "r+") as file:
                for line in file:
                    p = parse("{attr.type}={}", line)
                    if p is not None and p['attr.type'] == "Path":
                        line = 'Path=Profiles/xa6dylzk.clean\n'
                    profile += line
                file.seek(0)
                file.write(profile)
                file.truncate()
                file.close()

        return "OK"

    def download(self, url, file_name):
        import urllib.request

        # Download the file from `url` and save it locally under `file_name`:
        return urllib.request.urlretrieve(url, "install/" + file_name)

