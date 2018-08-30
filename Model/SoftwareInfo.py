from Model.Software import *
from Model.Logger import *
import errno, os, winreg
import platform

class SoftwareInfo:

    def __init__(self):
        self.proc_arch = os.environ['PROCESSOR_ARCHITECTURE'].lower()
        self.proc_arch64 = os.environ['PROCESSOR_ARCHITEW6432'].lower()
        self.WINDOWS = 'Windows'
        self.LINUX = "Linux"

    def get_all_software(self):

        #get the platform operating system.
        if platform.system() != self.WINDOWS:
            eprintlog(platform.system() + ' is not supported')
            return None

        item = []
        # proc_arch checked.
        if self.proc_arch == 'x86' and not self.proc_arch64:
            arch_keys = {0}
        elif self.proc_arch == 'x86' or self.proc_arch == 'amd64':
            arch_keys = {winreg.KEY_WOW64_32KEY, winreg.KEY_WOW64_64KEY}
        else:
            raise Exception("Unhandled arch: %s" % self.proc_arch)

        for arch_key in arch_keys:
            key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall", 0, winreg.KEY_READ | arch_key)
            for i in range(0, winreg.QueryInfoKey(key)[0]):
                skey_name = winreg.EnumKey(key, i)
                skey = winreg.OpenKey(key, skey_name)
                try:
                    soft = Software(winreg.QueryValueEx(skey, 'DisplayName')[0], winreg.QueryValueEx(skey, 'DisplayVersion')[0], winreg.QueryValueEx(skey, 'UninstallString')[0], winreg.QueryValueEx(skey, 'InstallLocation')[0])
                    item.append(soft)
                except OSError as e:
                    if e.errno == errno.ENOENT:
                        # DisplayName doesn't exist in this skey
                        pass
                finally:
                    skey.Close()

        var = ContainerSoft(item)
        return var

if __name__ == "__main__":
    lol = SoftwareInfo()
    print(lol.get_all_software().toJSON())


    import wmi


    c = wmi.WMI()
    items = []
    for p in c.Win32_Product():
        soft = Software()
        soft.name = format(p.PackageName)
        soft.uninstall = format(p.Vendor)
        soft.version = format(p.Version)
        soft.install = format(p.InstallLocation)
        items.append(soft)
        var = ContainerSoft(items)
    print(var.toJSON())