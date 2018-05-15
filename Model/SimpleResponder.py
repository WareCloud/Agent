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

from Model.Packet import Enum
from Model.Packet import PacketId, PacketError
from SimpleWebSocketServer import WebSocket

from Model import Command

clients = []
m_Command = Command.Command()


class SimpleResponder(WebSocket):

    def handleMessage(self):
        m_Command.set_websocket(self, clients[0])
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
        import time
        print(self.address, 'connected')
        clients.append(self)
        packet = PacketId()
        time.sleep(1)
        print(">> Server MSG: " + packet.toJSON())
        clients[0].sendMessage(packet.toJSON())

    def handleClose(self):
        print(self.address, 'closed')
        clients.pop()

