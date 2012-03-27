In order to run the various tests in this directory, you have to do the
following:

* Create a virtual environment for testing:
  ```virtualenv /tmp/bliss-test
     source /tmp/bliss-test/bin/activate```

* Install Bliss into the sandbox. From the Bliss ROOT DIRECTORY call:
  ```easy_install bliss```

* Now, change back to the test directory and run the tests, e.g.,:
  ```python testxyz.py```
