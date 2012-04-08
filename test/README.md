Bliss Test Suite
================

The Bliss Test Suite consists of two sets of independent tests: the unit tests
and the compliance tests. The unit tests are part of the test-driven
development approach in Bliss. They define tests for the Bliss API and runtime
system. The compliance tests is a set of independent tests that are run to
ensure the proper behavior of the different Bliss plug-ins. They are part of
the acceptance tests that are executed whenever a new plug-in is added to
Bliss. 

Unit Tests
----------

In order to run the unit tests, execute the following commands:

* Create a virtual environment for testing:
  ```virtualenv /tmp/bliss-test
     source /tmp/bliss-test/bin/activate```

* Install Bliss into the virutalenv sandbox. From the Bliss 
  ROOT DIRECTORY call:
  ```easy_install .```

* Once Bliss has installed successfully, you can run the unit tests by typing:
  ```python test/unittests.py```


Compliance Tests
----------------

In order to run the compliance tests for a specific adaptor, follow these steps:

* Open the configuration file __compliancetest.cfg__ and 
