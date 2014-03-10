import importme
import unittest
from Team import Team
from Task import Task
from Module import Module

class TestTask(unittest.TestCase):

    def setUp(self):
        pass

    def test_constructor(self):
        team = Team('test_team', 25, 10)
        self.assertTrue(team.name == 'test_team' and team.salary == 25 and team.size == 10)

    def test_calc_progress(self):
        team = Team('test_team', 25, 10)
        module = Module('test_module', 800)
        team.module = module

        while team.module and not team.module.completed:
            team.calc_progress()

        self.assertTrue(team.completed_modules and team.completed_modules[0] == module)



if __name__ == '__main__':
    unittest.main()
