import platform
import getpass
import os
import json

from Models import Configuration

class Enum:

    PACKET_ID = 1
    PACKET_ERROR = 20

    UNKN_CMD = "UNKN_CMD:"
    UNKN_PATH = "UNKN_PATH:"

    FAILED_INSTALL = "FAILED_INSTALL"
    FAILED_CONFIGURATION = "FAILED_CONFIGURATION"
    FAILED_UPDATE = "FAILED_UPDATE"
    FAILED_DOWNLOAD = "FAILED_DOWNLOAD"

    FAILED_FIND_INSTALLER = "FAILED_FIND_INSTALLER"
    FAILED_FIND_CONFIGURATION = "FAILED_FIND_CONFIGURATION"
    FAILED_FIND_DOWNLOAD = "FAILED_FIND_DOWNLOAD"


class PacketId:

    def __init__(self):
        self.id = Enum.PACKET_ID
        self.user = getpass.getuser()
        self.os = platform.system()
        self.path = os.path.dirname(os.path.abspath(__file__))
        self.version = "0.1.0"
        self.software = ""

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)


class PacketError:

    def __init__(self, cmd, type):
        self.id = Enum.PACKET_ERROR
        self.command = cmd
        self.type = type
        self.path = os.path.dirname(os.path.abspath(__file__))

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)


class PacketFollow:

    def __init__(self, cmd, state):
        self.id = Enum.PACKET_ERROR
        self.command = cmd
        self.state = type
        self.path = os.path.dirname(os.path.abspath(__file__))

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)