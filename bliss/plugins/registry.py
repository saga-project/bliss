# -*- coding: utf-8 -*-
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

__author__    = "Ole Christian Weidner"
__copyright__ = "Copyright 2011-2012, Ole Christian Weidner"
__license__   = "MIT"

_registry = []

_registry.append({"module"   : "bliss.plugins.local.localjob",  "class" : "LocalJobPlugin"})
_registry.append({"module"   : "bliss.plugins.ssh.job",         "class" : "SSHJobPlugin"})
_registry.append({"module"   : "bliss.plugins.sftp.sftpfile",   "class" : "SFTPFilesystemPlugin"})
_registry.append({"module"   : "bliss.plugins.sge.sgesshjob",   "class" : "SGEJobPlugin"})
_registry.append({"module"   : "bliss.plugins.pbs.pbsshjob",    "class" : "PBSJobPlugin"})
_registry.append({"module"   : "bliss.plugins.condor.condorjob","class" : "CondorJobPlugin"})

