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

* We assume that you have a locally cloned copy of Bliss (refered to as **[BLISS ROOT DIR]**).

* Create a virtual environment for testing:

        virtualenv /tmp/bliss-test
        source /tmp/bliss-test/bin/activate

* Install Bliss into the virutalenv sandbox. From the Bliss 
  **[BLISS ROOT DIR]** call:
  ```easy_install .```

* Once Bliss has installed successfully, you can run the unit tests by typing:
  ```python test/unittests.py```


Compliance Tests
----------------

In order to run the compliance tests for a specific adaptor, follow these steps:

* We assume that you have a locally cloned copy of Bliss (refered to as **[BLISS ROOT DIR]**).

* Create a virtual environment for testing (if not already done):

        virtualenv /tmp/bliss-test
        source /tmp/bliss-test/bin/activate

* Install Bliss into the virutalenv sandbox. From the Bliss 
  **[BLISS ROOT DIR]**, call:
  ```easy_install .```

* Next, run the individual test scripts with the URL of the adaptor/remote 
  machine combination you would like to test, e.g.,

  * ```python test/compliance/job/01_run_remote_exe.py ssh://peahi.inf.ed.ac.uk```
  * ```python test/compliance/job/02_run_shell_command_newline.py ssh://peahi.inf.ed.ac.uk```
  * ...
  
* You can add your test results manually to https://github.com/saga-project/bliss/blob/master/test/compliance/Readme.md

* If you think that you have discovered a bug, consider filing an issue: https://github.com/saga-project/bliss/issues


