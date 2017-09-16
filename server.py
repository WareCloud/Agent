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


HOST = ''
PORT = 8766
ERROR = "WrongCommand"
OK = "OK"

async def consumer(message):
    """ For receiving messages and passing them to a consumer coroutine: """
    print("Message received : {}".format(message))
    l_command_handler = Command.Command(message)
    if l_command_handler.is_valid_command() is True:
        return OK

    return ERROR

async def producer():
    """ For getting messages from a producer coroutine and sending them: """
    var = "OK"
    return var


async def handler(websocket, path):
    l_configuration = Configuration()
    name = "configuration"
    if l_configuration.has_conf_directory(name) is False:
        l_configuration.create_conf_directory(name)

    if l_configuration.has_soft_files(name) is False:
        l_configuration.create_conf_directory(name)

    name = "install"
    if l_configuration.has_conf_directory(name) is False:
        l_configuration.create_conf_directory(name)

    while True:
        name = await websocket.recv()
        return_message = await consumer(name)
        message = await producer()

        print("Message Sending : {}".format(return_message))
        await websocket.send(return_message)
        if return_message == ERROR:
            await websocket.close()



print("Initialisation du serveur")
start_server = websockets.serve(handler, '0', PORT)
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
