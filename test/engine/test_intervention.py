import importme
import unittest
from Intervention import Intervention

class TestIntervention(unittest.TestCase):

    def setUp(self):
        pass

    def test_constructor(self):
        intervention = Intervention('assign_specialist',"High","High")
        self.assertTrue(intervention.name == 'assign_specialist')
        self.assertTrue(intervention.cost == 4)
        self.assertTrue(intervention.impact == 4)

    def test_get_cost(self):
        intervention = Intervention('assign_specialist',"High","High")
        self.assertTrue(intervention.get_cost() == 500000)
        

if __name__ == '__main__':
    unittest.main()