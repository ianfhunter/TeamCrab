import importme
import unittest
from Task import Task

class TestTask(unittest.TestCase):

    def setUp(self):
        pass

    def test_constructor(self):
        task = Task('test_task', 60, 50, None)
        self.assertTrue(task.name == 'test_task' and task.actual_cost == 60 
        	             and task.expected_cost == 50 and not task.module)

if __name__ == '__main__':
    unittest.main()
