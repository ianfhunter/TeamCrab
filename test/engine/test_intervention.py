import importme
import unittest
from Intervention import Intervention

class TestIntervention(unittest.TestCase):

    def setUp(self):
        pass

    def test_constructor(self):
        intervention = Intervention('assign_specialist')
        self.assertTrue(intervention.typ == 'assign_specialist')

if __name__ == '__main__':
    unittest.main()