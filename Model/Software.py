import json

#
# Class Model of software
#

class Software:

    def __init__(self, name="", version="", uninstall="", InstallLocation=""):
        self.name = name
        self.version = version
        self.uninstall = uninstall
        self.install = InstallLocation

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)

class ContainerSoft:

    def __init__(self, array):
        self.arraySoft = array

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)