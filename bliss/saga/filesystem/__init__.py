# -*- coding: utf-8 -*-
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

''' B{File/Directory Management}

    The file managment API provides the ability to interact with (local and
    remote) file systems via the two classes, L{filesystem.Directory} and
    L{filesystem.File}. The API provides a number of operations, which all
    behave similar to the common unix command line tools (cp, ls, rm etc).

    B{Example}::

      # get a directory handle
      dir = saga.filesystem.Directory("sftp://localhost/tmp/")

      # create a subdir
      dir.make_dir ("data/")

      # list contents of the directory
      files = dir.list ()

      # copy *.dat files into the subdir
      for f in files :
          if re.match ('^.*\.dat$', f) :
              dir.copy (f, "sftp://localhost/tmp/data/")

    The above example covers most of the semantics of the filesystem package --
    additional capabilities, such get_size() or move(), can be found in the
    individual class documentations.
'''

__author__    = "Ole Christian Weidner"
__copyright__ = "Copyright 2011-2012, Ole Christian Weidner"
__license__   = "MIT"

from bliss.saga.filesystem.File import File
from bliss.saga.filesystem.Directory import Directory
