import unittest
from Model.Command import *

command = Command()


class ServerTest(unittest.TestCase):

    def test_set_websocket(self):
        server = 1
        client = 2
        command.set_websocket(server, client)
        self.assertEqual(command.server, 1)
        self.assertEqual(command.client, client)

    def test_new_command(self):
        string ="ceci est un test unitaire"
        tab = ["ceci", "est", "un", "test", "unitaire"]
        command.new_command(string)
        self.assertEqual(tab[0], command.parsed_command[0])
        self.assertEqual(tab[1], command.parsed_command[1])
        self.assertEqual(tab[2], command.parsed_command[2])
        self.assertEqual(tab[3], command.parsed_command[3])
        self.assertEqual(tab[4], command.parsed_command[4])

    def test_is_valid_command(self):
        string = "ceci est un test unitaire"
        command.new_command(string)
        self.assertEqual(False, command.is_valid_command())

        string = "install chrome.exe"
        command.new_command(string)
        self.assertEqual(True, command.is_valid_command())

    def test_follow(self):
        name = "follow System"
        command.new_command(name)
        packet = PacketError(name, PacketType.F_RUNNING, Enum.PACKET_FOLLOW)
        value = command.follow("System")
        self.assertEqual(packet.id, value.id)
        self.assertEqual("follow", value.command)
        self.assertEqual(packet.type, value.type)

        name = "follow toto.exe"
        command.new_command(name)
        packet = PacketError(name, PacketType.F_FINISH, Enum.PACKET_FOLLOW)
        value = command.follow("toto.exe")
        self.assertEqual(packet.id, value.id)
        self.assertEqual("follow", value.command)
        self.assertEqual(packet.type, value.type)


if __name__ == "__main__":
    unittest.main()
