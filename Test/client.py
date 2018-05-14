#!/usr/bin/env python3
# title				: client.py
# description		: fake client
# author			: Cloquet Alban
# date				: 2017/09/03
# version			: Python 3.6
# usage				: python client.py
# notes				: 
# python_version	: 3.6
# ==============================================================================

# Import the modules needed to run the script.

import websocket
import _thread
import time


def on_message(ws, message):
    print(message)


def on_error(ws, error):
    print(error)


def on_close(ws):
    print("### closed ###")


lol = []
def on_open(ws):
    def run(*args):
        p = 1
        for i in lol:
            time.sleep(p)
            ws.send(i)
            p += 3
        time.sleep(1)
        ws.close()
        print("thread terminating...")
    _thread.start_new_thread(run, ())


if __name__ == "__main__":
    websocket.enableTrace(True)
    # lol.append("error URL NAME")
    # lol.append("download https://stubdownloader.cdn.mozilla.net/builds/firefox-stub/fr/win/9705c66ad49acf77f0e875327f07d4ab65a4d7921dce9d41d6f421665a2b467b/Firefox%20Installer.exe FirefoxInstaller")
    # lol.append("error URL NAME")
    # lol.append("error URL NAME")
    # lol.append("error URL NAME")
    # lol.append("error URL NAME")
    lol.append("install tamere")
    # lol.append("install NppInstaller.exe")
    # lol.append("follow NppInstaller.exe")
    # lol.append("configure Notepad++ tamere")

    # lol.append("install FirefoxInstaller.exe")
    # lol.append("follow FirefoxInstaller.exe")
    # lol.append("follow FirefoxInstaller.exe")
    ws = websocket.WebSocketApp("ws://127.0.0.1:8000",
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)
    ws.on_open = on_open

    ws.run_forever()