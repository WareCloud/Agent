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
    lol.append("download_cfg https://api.warecloud.me/configs/Mozilla.tgz Mozilla.tgz")
    #lol.append("download https://stubdownloader.cdn.mozilla.net/builds/firefox-stub/en-US/win/a24e79e56c8dd45f6e865616580597def425efb223c7444ca6534bec5b8f4054/Firefox%20Installer.exe PPP")
    #lol.append("download https://stubdownloader.cdn.mozilla.net/builds/firefox-stub/en-US/win/a24e79e56c8dd45f6e865616580597def425efb223c7444ca6534bec5b8f4054/Firefox%20Installer.exe OOOOO")
    # lol.append("error URL NAME")
    # lol.append("error URL NAME")
    # lol.append("error URL NAME")
    # lol.append("error URL NAME")
    # lol.append("install tamere")
    # lol.append("install Notepad++.exe")
    # lol.append("follow NppInstaller.exe")
    # lol.append("configure Notepad++")

    #lol.append("install Firefox.exe")
    lol.append("uninstall Firefox")
    # lol.append("follow Firefox.exe")
    # lol.append("follow Firefox.exe")
    ws = websocket.WebSocketApp("ws://127.0.0.1:8000",
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)
    ws.on_open = on_open

    ws.run_forever()