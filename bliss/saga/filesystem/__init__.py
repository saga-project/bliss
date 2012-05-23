# -*- coding: utf-8 -*-
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

'''SAGA Filesystem Package API.

The SAGA filesystem package provides the ability to interact with (local and
remote) file systems.  The two provided classes, L{filesystem.Directory} and
L{filesystem.File} represent the well known abstractions common to all different
types of file systems.  The API provides a number of operations, which all
behave like the common unix command line tools (copy, list, remove etc)::

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
