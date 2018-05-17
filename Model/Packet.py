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

# Import the modules needed to run the script.

import platform
import getpass
import os
import json



class PacketType:
    UNKN_CMD = "UNKN_CMD:"
    UNKN_PATH = "UNKN_PATH:"

    F_RUNNING = "F_RUNNING"
    F_FINISH = "F_FINISH"
    F_ERROR = "CANT_FOUND"

    OK_INSTALL = "OK_INSTALL"
    OK_CONFIGURATION = "OK_CONFIGURATION"
    OK_UPDATE = "OK_UPDATE"
    OK_DOWNLOAD = "OK_DOWNLOAD"
    OK_UNINSTALL = "OK_UNINSTALL"

    FAILED_INSTALL = "FAILED_INSTALL"
    FAILED_FIND_INSTALLER = "FAILED_FIND_INSTALLER"
    FAILED_UNINSTALL = "FAILED_UNINSTALL"
    FAILED_FIND_UNINSTALLER = "FAILED_FIND_UNINSTALLER"

    FAILED_CONFIGURATION = "FAILED_CONFIGURATION"
    FAILED_UPDATE = "FAILED_UPDATE"
    FAILED_DOWNLOAD = "FAILED_DOWNLOAD"
    FAILED_FIND_CONFIGURATION = "FAILED_FIND_CONFIGURATION"
    FAILED_FIND_DOWNLOAD = "FAILED_FIND_DOWNLOAD"


class Enum:
    PACKET_ID = 1
    PACKET_INSTALL = 2
    PACKET_FOLLOW = 3
    PACKET_DOWNLOAD_STATE = 4
    PACKET_CONFIGURATION = 5
    PACKET_UNINSTALL = 6

    PACKET_ERROR = 20


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

    def __init__(self, cmd, type, id):
        self.id = id
        self.command = cmd
        self.type = type
        self.path = os.path.dirname(os.path.abspath(__file__))

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)


class Software:

    def __init__(self, software, path, id):
        self.id = software
        self.path = path

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)
