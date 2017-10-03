import pprint
import socket
import ssl
import threading
import unittest
import sys





# SET VARIABLES
packet, reply = "<packet>SOME_DATA</packet>", ""
HOST = '127.0.0.1'
PORT = 8000
CERTFILE = '../cert.pem'
KEYFILE = '../key.pem'


class TCPBase(threading.Thread):
    def __init__(self):
        self.soc = self.buildSocket()
        super(TCPBase, self).__init__()

    def buildSocket(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print('Socket created')
        return s



class ServerTest(unittest.TestCase):

    def test_connect(self):
        err = 0
        sock = TCPBase()
        try:
            ssl_sock = ssl.wrap_socket(sock.soc,
                                            ca_certs=CERTFILE,
                                            cert_reqs=ssl.CERT_REQUIRED)
            print("Wrapped client socket for SSL")
        except socket.error:
            print("SSL socket wrapping failed")
            err = 1

        if not err:
            try:
                ssl_sock.connect((HOST, PORT))
                print("client socket connected\n")
            except socket.error:
                print("Socket connection error in client: ", socket.error);
                err = 1
        if not err:
            print("send message")
            ssl_sock.sendall("Twas brillig and the slithy toves")

        sock.soc.close()
        ssl_sock.close()
        print("exit client")



    def test_constants(self):
        ssl.PROTOCOL_SSLv23
        ssl.PROTOCOL_SSLv3
        ssl.PROTOCOL_TLSv1
        ssl.CERT_NONE
        ssl.CERT_OPTIONAL
        ssl.CERT_REQUIRED


    def test_openssl_version(self):
        n = ssl.OPENSSL_VERSION_NUMBER
        t = ssl.OPENSSL_VERSION_INFO
        s = ssl.OPENSSL_VERSION
        self.assertIsInstance(n, (int, float))
        self.assertIsInstance(t, tuple)
        self.assertIsInstance(s, str)
        # Some sanity checks follow
        # >= 0.9
        self.assertGreaterEqual(n, 0x900000)
        # < 2.0
        self.assertLess(n, 0x20000000)
        major, minor, fix, patch, status = t
        self.assertGreaterEqual(major, 0)
        self.assertLess(major, 2)
        self.assertGreaterEqual(minor, 0)
        self.assertLess(minor, 256)
        self.assertGreaterEqual(fix, 0)
        self.assertLess(fix, 256)
        self.assertGreaterEqual(patch, 0)
        self.assertLessEqual(patch, 26)
        self.assertGreaterEqual(status, 0)
        self.assertLessEqual(status, 15)
        # Version string as returned by OpenSSL, the format might change
        self.assertTrue(s.startswith("OpenSSL {:d}.{:d}.{:d}".format(major, minor, fix)),
                        (s, t))

    def test_parse_cert(self):
        p = ssl._ssl._test_decode_cert(CERTFILE)
        sys.stdout.write("\n" + pprint.pformat(p) + "\n")



if __name__ == '__main__':
    unittest.main()
