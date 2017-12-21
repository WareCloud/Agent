import platform
import getpass
import os
import json

class Enum:

    PACKET_ID = 1
    PACKET_ERROR = 20

    UNKN_CMD = "UNKN_CMD:"
    UNKN_PATH = "UNKN_PATH:"

    FAILED_INSTALL = "FAILED_INSTALL:"
    FAILED_CONFIGURATION = "FAILED_CONFIGURATION:"
    FAILED_UPDATE = "FAILED_UPDATE:"
    FAILED_DOWNLOAD = "FAILED_DOWNLOAD:"


class PacketId:

    def __init__(self):
        self.id = Enum.PACKET_ID
        self.user = getpass.getuser()
        self.os = platform.system()
        self.path = os.path.dirname(os.path.abspath(__file__))

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