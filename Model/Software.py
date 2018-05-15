import json

#
# Class Model of software
#

class ContainerSoft:

    def __init__(self, array):
        self.arraySoft = array

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)


class Software:
    def __init__(self):
        self.name = ""
        self.version = ""
        self.vendor = ""
        self.location = ""
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)