from __future__ import print_function
import sys


def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


def eprintlog(*args, **kwargs):
    print(*args, file=sys.stdout, **kwargs)
    print(*args, file=open("AgentWareCloud.log", "a"), **kwargs)
