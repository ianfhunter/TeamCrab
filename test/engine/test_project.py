import importme
import unittest
from Project import Project
from RevenueTier import LowRevenueTier, MediumRevenueTier, HighRevenueTier
import datetime

class TestProject(unittest.TestCase):

    def setUp(self):
        pass

    def test_constructor(self):
        project = Project('test_project', 'Agile', 100000, LowRevenueTier())
        self.assertTrue(project.name == 'test_project' and project.development_method == 'Agile' 
            and project.cash == 100000 and project.expected_yearly_revenue == 1000000)

    def test_calc_nominal_schedule(self):
        project = Project('test_project', 'Agile', 45000, LowRevenueTier())
        project.calc_nominal_schedule(10)
        self.assertTrue(project.delivery_date == datetime.datetime(2014,1,1,0,0,0))

    def test_days_behind_schedule(self):
        project = Project('test_project', 'Agile', 200000, MediumRevenueTier())
        project.delivery_date = datetime.datetime(2014,1,3,0,0,0)

        project.current_time = datetime.datetime(2014,1,3,0,0,0)
        days = project.days_behind_schedule()
        self.assertTrue(days == 0)

        project.current_time = datetime.datetime(2014,1,1,0,0,0)
        days = project.days_behind_schedule()
        self.assertTrue(days == -2)

        project.current_time = datetime.datetime(2014,1,6,0,0,0)
        days = project.days_behind_schedule()
        self.assertTrue(days == 3)

    def test_game_score(self):
        project = Project('test_project', 'Agile', 200000, MediumRevenueTier())
        project.delivery_date = datetime.datetime(2014,1,3,0,0,0)
        project.current_time = datetime.datetime(2014,1,3,0,0,0)

        score = project.game_score()
        self.assertTrue(score == 2699996)

        project.current_time = datetime.datetime(2014,1,1,0,0,0)
        score = project.game_score()
        self.assertTrue(score == 2727773)

        project.current_time = datetime.datetime(2014,1,9,0,0,0)
        score = project.game_score()
        self.assertTrue(score == 2616662)

    def test_actual_budget(self):
        project = Project('test_project', 'Agile', 200000, LowRevenueTier())
        budget = project.actual_budget()

        self.assertTrue(budget == 0)

    def test_expected_revenue(self):
        project = Project('test_project', 'Agile', 200000, LowRevenueTier())
        revenue = project.expected_revenue()
        self.assertTrue(revenue == 500000)

        project = Project('test_project', 'Agile', 100000, MediumRevenueTier())
        revenue = project.expected_revenue()
        self.assertTrue(revenue == 2500000)

        project = Project('test_project', 'Agile', 500000, HighRevenueTier())
        revenue = project.expected_revenue()
        self.assertTrue(revenue == 10000000)

    def test_actual_revenue(self):
        project = Project('test_project', 'Agile', 200000, LowRevenueTier())
        project.delivery_date = datetime.datetime(2014,1,3,0,0,0)

        project.current_time = datetime.datetime(2014,1,3,0,0,0)
        revenue = project.actual_revenue()
        self.assertTrue(revenue == 500000.0)

        project.current_time = datetime.datetime(2014,1,1,0,0,0)
        revenue = project.actual_revenue()
        print revenue
        self.assertTrue(revenue == 505479.45)

if __name__ == '__main__':
    unittest.main()
