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
m_Command = Command.Command()


class SimpleResponder(WebSocket):

    def handleMessage(self):
        m_Command.new_command(self.data)
        print("<< Client MSG: " + self.data)
        if m_Command.is_valid_command() is True:
            packet = m_Command.run()
            print(">> Server MSG:", packet.type, packet.command)
            clients[0].sendMessage(packet.toJSON())
        else:
            packet = PacketError(m_Command.parsed_command[0], Enum.UNKN_CMD).toJSON()
            print(">> Server MSG: " + Enum.UNKN_CMD + self.data)
            clients[0].sendMessage(packet)

    def handleConnected(self):
        print(self.address, 'connected')
        clients.append(self)
        packet = PacketId()
        print(">> Server MSG: " + packet.toJSON())
        clients[0].sendMessage(packet.toJSON())

    def handleClose(self):
        print(self.address, 'closed')

