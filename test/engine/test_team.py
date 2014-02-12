import importme
import unittest
from Team import Team
from Task import Task
from Module import Module

class TestTask(unittest.TestCase):

    def setUp(self):
        pass

    def test_constructor(self):
        team = Team('test_team', 30, 25, 10)
        self.assertTrue(team.name == 'test_team' and team.efficiency == 30 and team.salary == 25 and team.size == 10)

    def test_calc_progress(self):
        team = Team('test_team', 30, 25, 10)
        module = Module('test_module', 800)
        team.task = module.get_task('design')

        team.calc_progress(1)
        self.assertFalse(team.task.completed)

        team.calc_progress(1)
        self.assertFalse(team.task.completed)

        team.calc_progress(1)
        self.assertFalse(team.task.completed)

        team.calc_progress(1)
        self.assertTrue(team.task.completed)

        self.assertTrue(module.completed_tasks and module.completed_tasks[0] == team.task)

if __name__ == '__main__':
    unittest.main()
