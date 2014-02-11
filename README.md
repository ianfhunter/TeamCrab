Software Engineering Simulator
======

## Group Project for CS4098 - Team Crab

In which you are a production manager in charge of various global software teams and you must try to complete your product with maximal cost efficiency.

## Requirements:
* python 2.7
* python-pygame
* python-nose

## Building, installing and everything in-between

The Makefile in the root of the project provides all functionality for building, testing and installing the project.
The file provides the following targets:

* build
* test
* clean
* install
* uninstall

The build target compiles each of the .py source files in the src directory into corresponding .pyc files in the bin 
directory (it will create the bin directory first if it does not already exist). The built project can then be run locally
via the command "./bin/SESimulator.pyc".

The test target will build the project as outlined above and then perform the unit tests which are in the test directory.
At the moment there are no tests since the project is only at a zero velocity release, so this target will perform the
same function as build for the time being.

The clean target deletes all the files in the bin directory.

The install target will first build the project (using the build target). It will then copy all the .pyc files in the 
bin directory into /opt/SESimulator. Then the script SESimulator.sh in the src directory will be copied into
/usr/local/bin/ so that users on the machine can start the simulator simply by using the command "SESimulator". Root
access is required to add files to opt/ and /usr/local/bin.

The uninstall target simply removes all SESimulator files from /opt and /usr/local/bin.

## Writing unit tests
The following is a simple example of the form a unit test should take in the test directory

```python
import importme
import unittest

class TestEngine(unittest.TestCase):

    def setUp(self):
        pass

    def test_method(self):
        pass

if __name__ == '__main__':
    unittest.main()
```

Each test directory contains an importme.py file. This must be imported at the start of each unit test. This allows
the test to see the modules contained in the bin directory at the root of the project.

Each file must contain a class which inherits from unittest.TestCase as shown. This provides a whole bunch of features
provided by the Python unittest framework. The setUp function must be provided to initialize any values required by each
test in this class. Every method that is a unittest must begin with "test_"

