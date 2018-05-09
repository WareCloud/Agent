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
import queue


clients = []


class SimpleResponder(WebSocket):

    def init(self):
        self.m_Command = Command.Command()

    def handleMessage(self):
        self.m_Command.new_command(self.data)
        print("<< Client MSG: " + self.data)
        if self.m_Command.is_valid_command() is True:
            self.m_Command.run()
            clients[0].sendMessage('{ "OK": OK }')
        else:
            packet = PacketError(self.m_Command.parsed_command[0], Enum.UNKN_CMD).toJSON()
            print(">> Server MSG: " + Enum.UNKN_CMD + self.data)
            clients[0].sendMessage(packet)

    def handleConnected(self):
        print(self.address, 'connected')
        clients.append(self)
        packet = PacketId()
        clients[0].sendMessage(packet.toJSON())


    def handleClose(self):
        print(self.address, 'closed')

