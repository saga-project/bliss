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

from bliss.saga.filesystem.file import File
from bliss.saga.filesystem.directory import Directory


Overwrite       =    1
'''Enforces an operation to continue even if the target entry does already
exist – if that flag is not given, an ’AlreadyExists’ exception would result
from such an operation.'''

Recursive       =    2
'''Enforces an operation to apply recursively on a directory tree – if that flag
is not given, the same operation would only apply to the given directory, and
not to its children.'''

Dereference     =    4
'''Enforces an operation to apply not to the entry pointed to by the target
name, but to the link target of that entry – if that flag is not given, the
same operation would apply to the entry directly, and its link target stays
unaffected.'''

Create          =    8
'''Allows a namespace entry to be created while opening it, if it does not
already exist – if that flag is not given, the same open operation would cause
a ’DoesNotExist’ exception. If the entry exists, the flag is ig- nored. This
flag implies the ’Write’ flag.'''

Exclusive       =   16
'''Implies a modification to the meaning of the Create flag: if the entry
already exists, the Create flag is is no longer silently ignored, but causes an
’AlreadyExists’ exception.'''

Lock            =   32
'''Enforces a lock on the name space entry when it is opened. Locks are
advisory in SAGA, semantic details for locking are defined in the description
of the open() call.'''

CreateParents   =   64
'''An operation which would create a name space entry would normally fail if
any path element in the targets name does not yet exist. If this flag is given,
such an operation would not fail, but would imply that the missing path
elements are created on the fly. This flag implies the ’Create’ flag.'''


