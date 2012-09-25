
File/Directory Management Overview
==================================

Introduction
------------

The file managment API provides the ability to interact with (local and
remote) file systems via the two classes, :class:`bliss.saga.filesystem.Directory` and
:class:`bliss.saga.filesystem.File`. The API provides a number of operations, which all
behave similar to the common unix command line tools (cp, ls, rm etc).

**Example**::

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


.. automodule:: bliss.saga.filesystem

