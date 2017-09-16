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

# Import the modules needed to run the script.
import asyncio
import websockets

from Models import Command
from directory import Configuration
import ssl
import signal
import sys
from SimpleWebSocketServer import WebSocket, SimpleWebSocketServer, SimpleSSLWebSocketServer
from optparse import OptionParser


HOST = ''
PORT = 8000
ERROR = "WrongCommand"
OK = "OK"

clients = []
class SimpleResponder(WebSocket):

    def handleMessage(self):
        for client in clients:
            print(self.data)
            l_command_handler = Command.Command(self.data)
            if l_command_handler.is_valid_command() is True:
                client.sendMessage(self.address[0] + u' - ' + OK)

    def handleConnected(self):
        print(self.address, 'connected')
        clients.append(self)

    def handleClose(self):
        print(self.address, 'closed')

if __name__ == "__main__":
    parser = OptionParser(usage="usage: %prog [options]", version="%prog 1.0")
    parser.add_option("--host", default='localhost', type='string', action="store", dest="host", help="hostname (localhost)")
    parser.add_option("--port", default=8000, type='int', action="store", dest="port", help="port (8000)")
    parser.add_option("--ssl", default=0, type='int', action="store", dest="ssl", help="ssl (1: on, 0: off (default))")
    parser.add_option("--cert", default='./cert.pem', type='string', action="store", dest="cert", help="cert (./cert.pem)")
    parser.add_option("--key", default='./key.pem', type='string', action="store", dest="key", help="key (./key.pem)")
    parser.add_option("--ver", default=ssl.PROTOCOL_TLSv1, type=int, action="store", dest="ver", help="ssl version")

    (options, args) = parser.parse_args()

    print("Initialisation du serveur")
    l_configuration = Configuration()
    name = "configuration"
    if l_configuration.has_conf_directory(name) is False:
        l_configuration.create_conf_directory(name)

    if l_configuration.has_soft_files(name) is False:
        l_configuration.create_conf_directory(name)

    name = "install"
    if l_configuration.has_conf_directory(name) is False:
        l_configuration.create_conf_directory(name)

    cls = SimpleResponder
    if options.ssl == 1:
        server = SimpleSSLWebSocketServer(options.host, options.port, cls, options.cert, options.key, version=options.ver)
    else:
        server = SimpleWebSocketServer(options.host, options.port, cls)


def close_sig_handler(signal, frame):
    server.close()
    sys.exit()


signal.signal(signal.SIGINT, close_sig_handler)

server.serveforever()