import importme
import unittest
import datetime

from engine import Project
from engine import Module
from engine import Location
from engine import RevenueTier
from engine import Team
from UI import logic

class TestModule(unittest.TestCase):

    def setUp(self):
        pass

    def test_total_person_hours(self):
        # Create dummy project
        p = Project.Project("Test Proj", "Agile", 1234, RevenueTier.LowRevenueTier())
        
        # Add placeholder locations, teams, modules to project
        m1 = Module.Module("Test Mod 1", 200)
        t1 = Team.Team("TT", 1, 1)
        t1.completed_modules = [m1]
        l1 = Location.Location("TestL", None, None, None, 123, None)
        l1.teams = [t1]
        
        m2 = Module.Module("Test Mod 1", 100)
        t2 = Team.Team("TT", 1, 1)
        t2.completed_modules = [m2]
        l2 = Location.Location("TestL", None, None, None, 123, None)
        l2.teams = [t2]
        
        # Add these locations to the project
        p.locations = [l1, l2]

        # Calculate total hours
        total, junk = logic.total_person_hours(p)
        self.assertTrue(total == 200 + 100)

    def test_report_table_line(self):
        # This is how a correctly formatted output looks
        expected_output = 'team           module       123   400             500          800       4 hrs        900 hrs'
        output = logic.report_table_line("team", "module", 123, 400, 500, 800, "4 hrs", "900 hrs") 
        self.assertTrue(expected_output == output)

    def test_generate_report(self):
        # Create dummy project
        p = Project.Project("Test Proj", "Agile", 1234, RevenueTier.LowRevenueTier())
         
        # Add placeholder locations, teams, modules to project
        m1 = Module.Module("Test Mod 1", 200)
        t1 = Team.Team("TT", 1, 1)
        t1.completed_modules = [m1]
        l1 = Location.Location("TestL", None, None, None, 123, None)
        l1.teams = [t1]
        
        m2 = Module.Module("Test Mod 1", 100)
        t2 = Team.Team("TT", 1, 1)
        t2.completed_modules = [m2]
        l2 = Location.Location("TestL", None, None, None, 123, None)
        l2.teams = [t2]
        
        # Add these locations to the project
        p.locations = [l1, l2]

        # Inject values into the project object
        p.development_method = "Agile" 
        p.delivery_date = datetime.datetime(2014,2,4,0,0,0)
        p.budget = 0
        p.cash = 12345600 
        p.expected_yearly_revenue = 20000000
        p.start_time = datetime.datetime(2014,1,1,0,0,0)
        p.current_time = datetime.datetime(2014,1,1,0,0,0)

        # Generate report
        report = logic.generate_report(p)

        # Make sure all fields of report are appropriate for their fields
        self.assertTrue(report["score"] == p.game_score())
        self.assertTrue(report["total_time"] == str(p.current_time - p.start_time))
        self.assertTrue(report["nominal_end_time"] == str(p.delivery_date))
        self.assertTrue(report["actual_end_time"] == str(p.current_time))
        self.assertTrue(report["days_behind_schedule"] == p.days_behind_schedule())
        self.assertTrue(report["expected_budget"] == p.expected_budget())
        self.assertTrue(report["actual_budget"] == p.actual_budget())
        self.assertTrue(report["expected_revenue"] == p.expected_revenue())
        self.assertTrue(report["actual_revenue"] == p.actual_revenue())
        self.assertTrue(report["endgame_cash"] == p.cash + p.actual_revenue())

if __name__ == '__main__':
    unittest.main()
