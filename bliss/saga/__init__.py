# -*- coding: utf-8 -*-
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

''' SAGA - A Simple API for Grid Applications
    =========================================

    Introduction
    ------------

    SAGA-Bliss is a light-weight Python package that implements parts of the U{OGF
    GFD.90 SAGA<www.gridforum.org/documents/GFD.90.pdf>}
    interface specification and provides plug-ins for different
    distributed middleware systems and services. SAGA-Bliss implements the most
    commonly used features of GFD.90 based upon extensive use-case analysis, and
    focuses on usability and simple deployment in real-world heterogeneous
    distributed computing environments and application scenarios.
   
    More information can be found at: U{http://saga-project.github.com/bliss}

    Saga Core API Classes
    ---------------------

    .. toctree::
       :maxdepth: 1
    
       Object.rst
       Error.rst
       Exception.rst
       Context.rst
       Session.rst
       Attributes.rst
       Url.rst

'''

__author__    = "Ole Christian Weidner, et al."
__copyright__ = "Copyright 2011-2012, Ole Christian Weidner"
__license__   = "MIT"

# Base "look-and-feel packages"
from bliss.saga.Url       import Url 
from bliss.saga.Object    import Object
from bliss.saga.Session   import Session 
from bliss.saga.Context   import Context
from bliss.saga.Exception import Exception 
from bliss.saga.Error     import Error 

# API packages
from bliss.saga           import filesystem
from bliss.saga           import resource
from bliss.saga           import job
