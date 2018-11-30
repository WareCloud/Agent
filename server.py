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
import urllib.request
from optparse import OptionParser
from Model.Configuration import Configuration
from Model.Packet import Enum, PacketType
from Model.Packet import PacketId, PacketError
from websocket_server import WebsocketServer
from Model import Command
from Model.SoftwareInfo import SoftwareInfo
from Model.Logger import *
from win10toast import ToastNotifier
import time

# To compile notification with python
import appdirs
from packaging import version
from packaging import specifiers
from packaging import requirements
from packaging import markers
# ====================================

PORT = 8000
CONFIGURATION = "configuration"
INSTALL = "install"
WARECLOUD = "///////////////////////////\n" \
            "/////////WARECLOUD/////////\n" \
            "///////////AGENT///////////\n" \
            "///////////////////////////\n"



# Called for every client connecting (after handshake)
def new_client(client, server):
    softwareInfo = SoftwareInfo()
    print(">>> New client [%d] connected" % client['id'])
    packet = PacketId()
    packet.software = softwareInfo.get_all_software()
    server.send_message(client, packet.toJSON())


# Called for every client disconnecting
def client_left(client, server):
    eprintlog("Client[%d] disconnected" % client['id'])

# Called when a client sends a message
def message_received(client, server, message):
    m_Command = Command.Command()
    m_Command.set_websocket(server, client)
    m_Command.new_command(message)
    eprintlog("<< Client MSG: " + message)
    if m_Command.is_valid_command() is True:
        packet = m_Command.run()
        if packet != None:
            eprintlog(">> Server MSG:", packet.type, packet.command)
            server.send_message(client, packet.toJSON())
    else:
        packet = PacketError(message, Enum.PACKET_ERROR, PacketType.UNKN_CMD)
        eprintlog(">> Server MSG: " + PacketType.UNKN_CMD, Enum.PACKET_ERROR)
        server.send_message(client, packet.toJSON())


def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


def portIsOpen(port):
    import socket, errno
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.bind(("0.0.0.0", int(port)))
    except socket.error as e:
        if e.errno == errno.EADDRINUSE:
            Logger.__call__().get_logger().debug(e)
        else:
            Logger.__call__().get_logger().debug(e)
        return False

    s.close()
    return True

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
        parser.add_option("--gui", default=0, type='int', action="store", dest="gui", help="GUI ?")
        (options, args) = parser.parse_args()

        """ Clean and create Log File """
        logger = Logger.__call__().get_logger()
        f = open("AgentWareCloud.log", "w")
        f.write("")
        f.close()
        eprintlog(WARECLOUD)

        opener = urllib.request.build_opener()
        opener.addheaders = [('User-agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36')]
        urllib.request.install_opener(opener)

        eprintlog(">> Configuration de l'agent ...")
        l_configuration = Configuration()
        l_configuration.create_directory(CONFIGURATION)
        l_configuration.create_directory(INSTALL)

        """ Start Server """
        if portIsOpen(options.port) is False:
            toaster = ToastNotifier()
            toaster.show_toast("Warecloud Agent", "Another program is using port " + str(options.port),
                               icon_path="brand-small.ico",
                               duration=2, threaded=True)
            while toaster.notification_active(): time.sleep(0.2)
            exit(1)

        eprintlog(">> Running on port :[", options.port, "] ...")
        server = WebsocketServer(options.port, '0.0.0.0')
        server.set_fn_new_client(new_client)
        server.set_fn_client_left(client_left)
        server.set_fn_message_received(message_received)
        server.run_forever().start()
    else:
        toaster = ToastNotifier()
        toaster.show_toast("Warecloud Agent", "Run As Admin",
                           icon_path="brand-small.ico",
                           duration=2, threaded=True)
        while toaster.notification_active(): time.sleep(0.2)



