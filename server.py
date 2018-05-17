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

import ssl
import ctypes, sys
from optparse import OptionParser
from Model.Configuration import Configuration
from Model.Packet import Enum, PacketType
from Model.Packet import PacketId, PacketError
from websocket_server import WebsocketServer
from Model import Command
from Model.eprint import eprintlog

PORT = 8000
CONFIGURATION = "configuration"
INSTALL = "install"
WARECLOUD = "///////////////////////////\n" \
            "/////////WARECLOUD/////////\n" \
            "///////////AGENT///////////\n" \
            "///////////////////////////\n"

m_Command = Command.Command()

# Called for every client connecting (after handshake)
def new_client(client, server):
    import time
    time.sleep(1)
    print("New client connected and was given id %d" % client['id'])
    packet = PacketId()
    server.send_message(client, packet.toJSON())


# Called for every client disconnecting
def client_left(client, server):
    eprintlog("Client(%d) disconnected" % client['id'])


# Called when a client sends a message
def message_received(client, server, message):
    m_Command.set_websocket(server, client)
    m_Command.new_command(message)
    eprintlog("<< Client MSG: " + message)
    if m_Command.is_valid_command() is True:
        packet = m_Command.run()
        if packet != None:
            eprintlog(">> Server MSG:", packet.type, packet.command)
            server.send_message(client, packet.toJSON())
    else:
        packet = PacketError(m_Command.parsed_command[0], Enum.PACKET_ERROR, PacketType.UNKN_CMD)
        eprintlog(">> Server MSG: " + PacketType.UNKN_CMD, Enum.PACKET_ERROR)
        server.send_message(client, packet.toJSON())


def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

if __name__ == "__main__":
    if is_admin():
        parser = OptionParser(usage="usage: %prog [options]", version="%prog 1.0")
        parser.add_option("--host", default='0.0.0.0', type='string', action="store", dest="host", help="hostname (localhost)")
        parser.add_option("--port", default=PORT, type='int', action="store", dest="port", help="port (8000)")
        parser.add_option("--ssl", default=0, type='int', action="store", dest="ssl", help="ssl (1: on, 0: off (default))")
        parser.add_option("--cert", default='./cert.pem', type='string', action="store", dest="cert", help="cert (./cert.pem)")
        parser.add_option("--key", default='./key.pem', type='string', action="store", dest="key", help="key (./key.pem)")
        parser.add_option("--ver", default=ssl.PROTOCOL_TLSv1, type=int, action="store", dest="ver", help="ssl version")
        parser.add_option("--debug", default=0, type='int', action="store", dest="debug", help="debug option")
        (options, args) = parser.parse_args()

        file = open("AgentWareCloud.log", "w")
        file.write("")
        file.close()

        eprintlog(WARECLOUD)

        if options.debug == 0:
            eprintlog(">> Configuration de l'agent ...")

        l_configuration = Configuration()
        if l_configuration.has_directory(CONFIGURATION) is False:
            l_configuration.create_directory(CONFIGURATION)
        if l_configuration.has_directory(INSTALL) is False:
            l_configuration.create_directory(INSTALL)

        """ Lancement du serveur """
        if options.debug == 0:
            eprintlog(">> Lancement du serveur ...")

        l_configuration.get_all_software()

        server = WebsocketServer(8000, '0.0.0.0')
        server.set_fn_new_client(new_client)
        server.set_fn_client_left(client_left)
        server.set_fn_message_received(message_received)
        eprintlog(">> Running on port :[", PORT, "] ...")
        server.run_forever()
    else:
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)




