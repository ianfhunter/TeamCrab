import unittest
import importme
import types
from engine import Project

import re,glob,sys
import os
from os import listdir
import fnmatch

class TestModule(unittest.TestCase):

    def setUp(self):
        pass

    def test_function_coverage(self):
        matches = []
        to_test = []
	#get all function names from src/
        for root, dirnames, filenames in os.walk('../src'):
            for filename in fnmatch.filter(filenames, '*.py'):
                matches.append(os.path.join(root, filename))
        for pyfile in matches:
            for line in open(pyfile):
	        if "def" in line:
                   result = re.search("def .*\(",line)
                   if result:
                       result = result.group()[4:-1]
		       to_test.append(result)
#                       print result ,"\t\t" , pyfile 

	print "=========TEST FNs========="
	matches = []
        for root, dirnames, filenames in os.walk('../test'):
            for filename in fnmatch.filter(filenames, '*.py'):
                matches.append(os.path.join(root, filename))
        for pyfile in matches:
            for line in open(pyfile):
	        if "def" in line:
                   result = re.search("def .*\(",line)
                   if result:
                       result_nohead = result.group()[9:-1]
                       if result_nohead in to_test:
			   to_test.remove(result_nohead)
                           print "Matched"
	for test in to_test:
	    print test + "()"
			
	return True


if __name__ == '__main__':
    unittest.main()
