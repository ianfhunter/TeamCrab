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

    def test_current_cost(self):
        for i in range(50, 100):
            task = Task('test_task', i, 50, None)
            self.assertTrue(task.current_cost() == i)

    def test_increase_cost(self):
        task = Task('test_task', 50, 50, None)
        cost = 50
        for i in range(100, 150):
            cost += i
            task.increase_cost(i)
            self.assertTrue(task.actual_cost == cost)

if __name__ == '__main__':
    unittest.main()
