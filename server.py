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

import signal
import ssl
import sys
from optparse import OptionParser

from SimpleWebSocketServer import SimpleWebSocketServer, SimpleSSLWebSocketServer

from Models.Configuration import Configuration
from Models.SimpleResponder import SimpleResponder

PORT = 8000
CONFIGURATION = "configuration"
INSTALL = "install"

def close_sig_handler(signal, frame):
    server.close()
    sys.exit()

if __name__ == "__main__":
    parser = OptionParser(usage="usage: %prog [options]", version="%prog 1.0")
    parser.add_option("--host", default='localhost', type='string', action="store", dest="host", help="hostname (localhost)")
    parser.add_option("--port", default=PORT, type='int', action="store", dest="port", help="port (8000)")
    parser.add_option("--ssl", default=0, type='int', action="store", dest="ssl", help="ssl (1: on, 0: off (default))")
    parser.add_option("--cert", default='./cert.pem', type='string', action="store", dest="cert", help="cert (./cert.pem)")
    parser.add_option("--key", default='./key.pem', type='string', action="store", dest="key", help="key (./key.pem)")
    parser.add_option("--ver", default=ssl.PROTOCOL_TLSv1, type=int, action="store", dest="ver", help="ssl version")
    parser.add_option("--debug", default=True, type=bool, action="store", dest="debug", help="debug option")

    (options, args) = parser.parse_args()

    """ Configuration de l'agent """
    l_configuration = Configuration()
    if l_configuration.has_directory(CONFIGURATION) is False:
        l_configuration.create_directory(CONFIGURATION)

    if l_configuration.has_files(CONFIGURATION) is False:
        l_configuration.create_directory(CONFIGURATION)

    if l_configuration.has_directory(INSTALL) is False:
        l_configuration.create_directory(INSTALL)

    """ Lancement du serveur """
    cls = SimpleResponder
    if options.ssl == 1:
        server = SimpleSSLWebSocketServer(options.host, options.port, cls, options.cert, options.key, version=options.ver)
    else:
        server = SimpleWebSocketServer(options.host, options.port, cls)

    signal.signal(signal.SIGINT, close_sig_handler)
    server.serveforever()




