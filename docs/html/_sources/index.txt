
Bliss, a SAGA implementation in Python
======================================

Bliss (\ **B**\ liss **IS** **S**\ AGA) is a pragmatic, light-weight
implementation of the OGF SAGA standard (GFD.90_). Bliss is written 100% in
Python and focuses on usability and ease of deployment rather than on feature
completeness or strict standard obedience.

Please refer to the Bliss wiki_ for installation instructions, user guide, etc:

.. _wiki:   http://www.github.com/saga-project/bliss/wiki/
.. _GFD.90: http://www.ogf.org/documents/GFD90.pdf


Bliss API documentation
=======================

Bliss API overview and Core classes
-----------------------------------

.. toctree::
   :maxdepth: 1

   bliss/saga/__init__
   bliss/saga/Object
   bliss/saga/Error
   bliss/saga/Exception
   bliss/saga/Context
   bliss/saga/Session
   bliss/saga/Attributes
   bliss/saga/Url


The Job API Package
-------------------

.. toctree::
   :maxdepth: 1

   bliss/saga/job/__init__
   bliss/saga/job/Description
   bliss/saga/job/Service
   bliss/saga/job/Job


The Resource API Package
------------------------

.. toctree::
   :maxdepth: 1

   bliss/saga/resource/__init__
   bliss/saga/resource/Manager
   bliss/saga/resource/State
   bliss/saga/resource/ComputeDescription
   bliss/saga/resource/Compute
   bliss/saga/resource/StorageDescription
   bliss/saga/resource/Storage




The Filesystem API Package
--------------------------

.. toctree::
   :maxdepth: 1

   bliss/saga/filesystem/__init__
   bliss/saga/filesystem/Directory
   bliss/saga/filesystem/File



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`


----------

**Footnote**:

This documentation was build with the following command::
  
    .../bliss/ >   sphinx-build -a -E -n -c docs/ -b html . docs/html

