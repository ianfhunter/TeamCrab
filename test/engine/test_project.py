import importme
import unittest
from Project import Project
from Location import Location
from RevenueTier import LowRevenueTier, MediumRevenueTier, HighRevenueTier
import datetime
from global_config import config
import sys

class TestProject(unittest.TestCase):

    def setUp(self):
        pass

    def test_constructor(self):
        project = Project('test_project', 'Agile', 100000, LowRevenueTier())
        self.assertTrue(project.name == 'test_project' and project.development_method == 'Agile' 
            and project.cash == 100000 and project.expected_yearly_revenue == 1000000)

    def test_calc_nominal_schedule(self):
        project = Project('test_project', 'Agile', 45000, LowRevenueTier())
        project.calc_nominal_schedule()
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
        tmp = project.cash
        project.cash = 0

        score = project.game_score()
        self.assertTrue(score == 2500000)

        project.cash = 10000
        project.current_time = datetime.datetime(2014,1,2,0,0,0)
        score = project.game_score()
        self.assertTrue(score == 2523698)

        project.cash = -10000
        project.current_time = datetime.datetime(2014,1,4,0,0,0)
        score = project.game_score()
        self.assertTrue(score == 2473801)

        tmp = project.cash

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

    def test_add_intervention(self):
        project = Project('test_project', 'Agile', 200000, LowRevenueTier())
        project.locations =  [Location('Rio de Janeiro', "Brazilian", 30),Location('New Dehli', "Indian", 30)];
        startng_cash = project.cash

        project.add_intervention("Rio de Janeiro","Reduce interaction between teams")

        #Intervention added
        self.assertTrue(project.locations[0].intervention_list[0] == "Reduce interaction between teams")
        #Intevention Level Raised
        self.assertTrue(project.locations[0].intervention_level == 1)
        #Cash removed
        self.assertTrue(project.cash < startng_cash)


        pass

if __name__ == '__main__':
    unittest.main()
