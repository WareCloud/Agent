#!/usr/bin/env python3
# title				: server.py
# description		: Unitary Test
# author			: Cloquet Alban
# date				: 2017/06/19
# version			: Python 3.6
# usage				: UT
# notes				:
# python_version	: 3.6
# ==============================================================================

# ////////////////////////////////////////////////////////////////////////////////
# //
# //  WARECLOUD
# //
# ////////////////////////////////////////////////////////////////////////////////

import unittest
from Model.Command import *

class ServerTest(unittest.TestCase):

    def test_set_websocket(self):
        command = Command()
        server = 1
        client = 2
        command.set_websocket(server, client)
        self.assertEqual(command.server, 1)
        self.assertEqual(command.client, client)

    def test_new_command(self):
        command = Command()
        name = '{"command":"follow","software":{"name":"System","file":"System.exe","url":null,"path":null,"extension":null}}'
        command.new_command(name)
        self.assertEqual("follow", command.parsed_command.command)
        self.assertEqual("System", command.parsed_command.software.name)

    def test_is_valid_command(self):
        command = Command()
        string = "ceci est un test unitaire"
        command.new_command(string)
        self.assertEqual(False, command.is_valid_command())

        string = '{"command":"follow","software":{"name":"System","file":"System.exe","url":null,"path":null,"extension":null}}'
        command.new_command(string)
        self.assertEqual(True, command.is_valid_command())

    def test_follow(self):
        command = Command()
        name = '{"command":"follow","software":{"name":"System","file":"slack.exe","url":null,"path":null,"extension":null}}'
        command.new_command(name)
        packet = PacketError(command.parsed_command.software.file, PacketType.F_RUNNING, Enum.PACKET_FOLLOW)
        value = command.follow()
        self.assertEqual(packet.id, value.id)
        self.assertEqual("slack.exe", value.command)
        self.assertEqual(packet.type, value.type)

        command = Command()
        name = '{"command":"follow","software":{"name":"Toto","file":"Toto.exe","url":null,"path":null,"extension":null}}'
        command.new_command(name)
        packet = PacketError(command.parsed_command.software.file, PacketType.F_FINISH, Enum.PACKET_FOLLOW)
        value = command.follow()
        self.assertEqual(packet.id, value.id)
        self.assertEqual("Toto.exe", value.command)
        self.assertEqual(packet.type, value.type)


if __name__ == "__main__":
    unittest.main()
