import importme
import unittest
from Project import Project

class TestProject(unittest.TestCase):

    def setUp(self):
        pass

    def test_constructor(self):
        project = Project('test_project', 'Agile', (3, 3, 2014))
        self.assertTrue(project.name == 'test_project' and project.development_method == 'Agile' 
            and project.delivery_date == (3, 3, 2014))

if __name__ == '__main__':
    unittest.main()
