#!/usr/bin/env python3
# title				: Configuration.py
# description		: class to manage configuration
# author			: Cloquet Alban
# date				: 2017/08/20
# version			: Python 3.6
# usage				: python Configuration.py
# notes				:
# python_version	: 3.6
# ==============================================================================

from Model.Logger import *
import errno
import os


class Configuration:

    def __init__(self):
        """Setup configuration"""
        self.files = [f for f in os.listdir('.')]
        self.current = os.getcwd()


    def  __has_directory(self, name):
        for f in self.files:
            if f == name:
                return True
        return False

    def create_directory(self, name):
        if self.__has_directory(name) is False:
            try:
                os.makedirs(name)
                eprintlog("Sucessfully created directory: ", name)
            except OSError as e:
                if e.errno != errno.EEXIST:
                    raise

