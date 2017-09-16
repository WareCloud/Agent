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


def on_open(ws):
    def run(*args):
        for i in range(30000):
            time.sleep(1)
            ws.send("download URL NAME")#"Hello %d" % i)
        time.sleep(1)
        ws.close()
        print("thread terminating...")
    _thread.start_new_thread(run, ())


if __name__ == "__main__":
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp("ws://127.0.0.1:8766",
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)
    ws.on_open = on_open

    ws.run_forever()