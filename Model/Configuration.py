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
import platform


from Model import Software


class Configuration:

    def __init__(self):
        """Setup configuration"""
        self.files = [f for f in os.listdir('.')]
        self.current = os.getcwd()
        self.WINDOWS = 'Windows'
        self.LINUX = "Linux"

    def has_directory(self, name):
        for f in self.files:
            if f == name:
                return True
        return False

    def has_files(self, name):
        os.chdir(name)
        files = [f for f in os.listdir('.')]
        for f in files:
            if f == "software":
                os.chdir("..")
                return True
        os.chdir("..")
        return False

    def create_directory(self, name):
        try:
            os.makedirs(name)
            eprintlog("Sucessfully created directory: ", name)
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise

    def create_files(self, name):
        try:
            open(name, 'a').close()
            eprintlog("Sucessfully created files: ", name)
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise

        self.get_all_software()

    def get_all_software(self):
        return ""
        eprintlog(platform.system())
        if platform.system() != self.WINDOWS:
            self.logger.info(platform.system() + ' is not supported')
            return None

       # if os.stat("software").st_size != 0:
        #    self.logger.info('File already exist ')
         #   print("Software file already exist:")
      #      return None

        import wmi
        eprintlog("Software Initialisation")
        c = wmi.WMI()
        items = []
        for p in c.Win32_Product():
            soft = Software.Software()
            soft.name = format(p.PackageName)
            soft.vendor = format(p.Vendor)
            soft.version = format(p.Version)
            soft.location = format(p.InstallLocation)
            items.append(soft)
        var = Software.ContainerSoft(items)
        open("software", 'w').write(var.toJSON())
        return var.toJSON()
