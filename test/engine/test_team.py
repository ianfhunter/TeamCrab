import importme
import unittest
from Team import Team
from Task import Task
from Module import Module
import datetime

class TestTask(unittest.TestCase):

    def setUp(self):
        pass

    def test_constructor(self):
        team = Team('test_team', 25, 10)
        self.assertTrue(team.name == 'test_team' and team.salary == 25 and team.size == 10)

    def test_calc_progress(self):
        current_time = datetime.datetime(2014,1,1,0,0,0)
        team = Team('test_team', 25, 10)
        module = Module('test_module', 800)
        module.calc_deadline(current_time, 10)
        team.module = module

        while team.module and not team.module.completed:
            current_time += datetime.timedelta(hours=1)
            team.calc_progress(current_time)

        self.assertTrue(team.completed_modules and team.completed_modules[0] == module)



if __name__ == '__main__':
    unittest.main()
