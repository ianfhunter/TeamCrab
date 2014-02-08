import unittest

class TestSequenceFunctions(unittest.TestCase):

    def setUp(self):           #this is run before any below tests
        self.seq = range(10)

    def test_shuffle(self):    #all tests start with "test_"
        self.assertEqual(2,1+1)

if __name__ == '__main__':
    unittest.main()