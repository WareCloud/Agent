import sys
from cx_Freeze import setup, Executable


include_files = ['autorun.inf']
base = None

if sys.platform == "win32":
    base = "Win32GUI"

setup(
    name='Agent',
    version='0.1',
    options={'build.exe': {'include_files': include_files,
                           "icon": "brand-small.ico"}},
    executables=[Executable("server.py", base=base)],
    url='https://github.com/WareCloud/Agent',
    license='Warecloud',
    author='Cloquet Alban',
    author_email='clouqet.alban@epitech.eu',
    description='AgentWarecloud'
)
