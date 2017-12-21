#!/usr/bin/env python3
# title				: SimpleResponder.py
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

from SimpleWebSocketServer import WebSocket

from Models import Command
from Models.Packet import Enum
from Models.Packet import PacketId, PacketError

clients = []


class SimpleResponder(WebSocket):

    def handleMessage(self):
        l_command_handler = Command.Command(self.data)
        print("CMSG: " + self.data)
        if l_command_handler.is_valid_command() is True:
            packet = str(self.address[0] + self.data)
        else:
            packet = PacketError(l_command_handler.m_command[0], Enum.UNKN_CMD).toJSON()
            print("SMSG: " + Enum.UNKN_CMD + self.data)

        clients[0].sendMessage(packet)

    def handleConnected(self):
        print(self.address, 'connected')
        clients.append(self)
        packet = PacketId()
        clients[0].sendMessage(packet.toJSON())


    def handleClose(self):
        print(self.address, 'closed')

