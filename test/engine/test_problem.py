import importme
import unittest
from Problem import Problem

class TestProblem(unittest.TestCase):

    def setUp(self):
        pass

    def test_constructor(self):
        problem = Problem('flood', 200)
        self.assertTrue(problem.typ == 'flood' and problem.cost == 200)

if __name__ == '__main__':
    unittest.main()
