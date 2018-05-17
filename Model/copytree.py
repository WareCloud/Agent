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

from Model.Logger import *
import os
import shutil
import stat

def copytree(src, dst, symlinks = False, ignore = None):
      Logger.__call__().get_logger().info("SRC=" + src)
      Logger.__call__().get_logger().info("DST=" + dst)
      if not os.path.exists(dst):
        os.makedirs(dst)
        shutil.copystat(src, dst)
      lst = os.listdir(src)
      if ignore:
        excl = ignore(src, lst)
        lst = [x for x in lst if x not in excl]
      for item in lst:
        s = os.path.join(src, item)
        d = os.path.join(dst, item)
        if symlinks and os.path.islink(s):
          if os.path.lexists(d):
            os.remove(d)
          os.symlink(os.readlink(s), d)
          try:
            st = os.lstat(s)
            mode = stat.S_IMODE(st.st_mode)
            os.lchmod(d, mode)
          except:
            pass # lchmod not available
        elif os.path.isdir(s):
          copytree(s, d, symlinks, ignore)
        else:
            try:
                shutil.copy2(s, d)
            except IOError as e:
                Logger.__call__().get_logger().info("Unable to copy file. " + e.filename)



