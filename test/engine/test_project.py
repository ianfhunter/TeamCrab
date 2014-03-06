import importme
import unittest
from Project import Project
from RevenueTier import LowRevenueTier

class TestProject(unittest.TestCase):

    def setUp(self):
        pass

    def test_constructor(self):
        project = Project('test_project', 'Agile', 100000, LowRevenueTier())
        self.assertTrue(project.name == 'test_project' and project.development_method == 'Agile' 
            and project.budget == 100000 and project.expected_yearly_revenue == 1000000)

if __name__ == '__main__':
    unittest.main()
