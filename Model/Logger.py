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

from __future__ import print_function
import logging
from datetime import datetime
import os
import sys

class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Logger(metaclass=Singleton):
    _logger = None

    def __init__(self):
        self._logger = logging.getLogger("crumbs")
        self._logger.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s [%(levelname)s | %(filename)s:%(lineno)s] > %(message)s')

        now = datetime.now()
        dirname = "./log"

        if not os.path.isdir(dirname):
            os.mkdir(dirname)
        fileHandler = logging.FileHandler(dirname + "/log_" + now.strftime("%Y-%m-%d") + ".log")
        fileHandler.setFormatter(formatter)
        self._logger.addHandler(fileHandler)
        print("Generate new instance")
        self._logger.info("=======================================================================")

    def get_logger(self):
        return self._logger

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

def eprintlog(*args, **kwargs):
    print(*args, file=sys.stdout, **kwargs)
    print(*args, file=open("AgentWareCloud.log", "a"), **kwargs)