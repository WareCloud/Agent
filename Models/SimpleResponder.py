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

clients = []


class SimpleResponder(WebSocket):

    def handleMessage(self):
        for client in clients:
            print(self.data)
            l_command_handler = Command.Command(self.data)
            if l_command_handler.is_valid_command() is True:
                client.sendMessage(self.address[0] + u' - ')

    def handleConnected(self):
        print(self.address, 'connected')
        clients.append(self)

    def handleClose(self):
        print(self.address, 'closed')
