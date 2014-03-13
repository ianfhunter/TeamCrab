import importme
import unittest
from Location import Location
from Module import Module
from global_config import cultures
from Team import Team

class TestLocation(unittest.TestCase):

    def setUp(self):
        pass

    def test_constructor(self):
        location = Location('Dublin', 0, "culture1", 30, 25,(375,148))
        self.assertTrue(location.name == 'Dublin' and location.time_zone == 0 and location.culture == "culture1"
            and location.capacity == 30 and location.salary == 25 and not location.teams and not location.specialists)

    def test_add_team(self):
        location = Location('Dublin', 0, "culture1", 30, 25,(375,148))

        team1 = Team('test_team1', 25, 10)
        self.assertTrue(location.add_team(team1))

        team2 = Team('test_team2', 20, 20)
        self.assertTrue(location.add_team(team2))

        team3 = Team('test_team3', 20, 1)
        self.assertFalse(location.add_team(team3))

        self.assertTrue(len(location.teams) == 2)

    def test_num_teams(self):
        location = Location('Dublin', 0, "culture1", 30, 25,(375,148))

        self.assertTrue(location.num_teams() == 0)

        location.add_team(Team('test_team1', 25, 1))
        location.add_team(Team('test_team2', 25, 1))

        self.assertTrue(location.num_teams() == 2)

        location.add_team(Team('test_team3', 25, 1))

        self.assertTrue(location.num_teams() == 3)

        location.add_team(Team('test_team4', 25, 1))
        location.add_team(Team('test_team5', 25, 1))

        self.assertTrue(location.num_teams() == 5)

    def test_total_module_progress(self):
        location = Location('Dublin', 0, "culture1", 30, 25,(375,148))

        location.add_team(Team('test_team1', 25, 1))
        location.add_team(Team('test_team2', 25, 1))
        location.add_team(Team('test_team3', 25, 1))
        location.add_team(Team('test_team4', 25, 1))
        location.add_team(Team('test_team5', 25, 1))

        self.assertTrue(location.total_module_progress() == 0)


    def test_num_modules_on_schedule(self):
        location = Location('Dublin', 0, "culture1", 30, 25,(375,148))

        location.add_team(Team('test_team1', 25, 1))
        location.teams[0].module = Module('test_module1', 600)
        
        self.assertTrue(location.num_modules_on_schedule() == 1)

        location.add_team(Team('test_team2', 25, 1))
        location.teams[1].module = Module('test_module2', 400)

        location.add_team(Team('test_team3', 25, 1))
        location.teams[2].module = Module('test_module3', 200)

        self.assertTrue(location.num_modules_on_schedule() == 3)

        location.add_team(Team('test_team4', 25, 1))
        location.teams[3].module = Module('test_module4', 600)

        location.add_team(Team('test_team5', 25, 1))
        location.teams[4].module = Module('test_module5', 800)

        self.assertTrue(location.num_modules_on_schedule() == 5)

    def test_num_modules(self):
        location = Location('Dublin', 0, "culture1", 30, 25,(375,148))

        location.add_team(Team('test_team1', 25, 1))
        location.teams[0].module = Module('test_module1', 600)
        
        self.assertTrue(location.num_modules() == 1)

        location.add_team(Team('test_team2', 25, 1))
        location.teams[1].module = Module('test_module2', 400)

        location.add_team(Team('test_team3', 25, 1))
        location.teams[2].module = Module('test_module3', 200)

        self.assertTrue(location.num_modules() == 3)

        location.add_team(Team('test_team4', 25, 1))
        location.teams[3].module = Module('test_module4', 600)

        location.add_team(Team('test_team5', 25, 1))
        location.teams[4].module = Module('test_module5', 800)

        self.assertTrue(location.num_modules() == 5)

    def test_geo_distance(self):
        location1 = Location('test', 0, "culture1", 30, 25,(375,0))
        location2 = Location('test', 0, "culture1", 30, 25,(100, 0))

        self.assertTrue(location1.geo_distance(location2) == 4.0)

        location3 = Location('test', 0, "culture1", 30, 25,(100, 100))
        location4 = Location('test', 0, "culture1", 30, 25,(100, 0))

        self.assertTrue(location3.geo_distance(location4) == 3.0)

        location5 = Location('test', 0, "culture1", 30, 25,(100, 100))
        location6 = Location('test', 0, "culture1", 30, 25,(93, 90))

        self.assertTrue(location5.geo_distance(location6) == 2.0)

        location7 = Location('test', 0, "culture1", 30, 25,(100, 100))
        location8 = Location('test', 0, "culture1", 30, 25,(100, 98))

        self.assertTrue(location7.geo_distance(location8) == 1.0)

    def test_temp_distance(self):
        location1 = Location('test', 0, "culture1", 30, 25,(375,0))
        location2 = Location('test', 11, "culture1", 30, 25,(100, 0))

        self.assertTrue(location1.temp_distance(location2) == 4.0)

        location3 = Location('test', 1, "culture1", 30, 25,(100, 100))
        location4 = Location('test', 9, "culture1", 30, 25,(100, 0))

        self.assertTrue(location3.temp_distance(location4) == 3.0)

        location5 = Location('test', 4, "culture1", 30, 25,(100, 100))
        location6 = Location('test', 9, "culture1", 30, 25,(93, 90))

        self.assertTrue(location5.temp_distance(location6) == 2.0)

        location7 = Location('test', 2, "culture1", 30, 25,(100, 100))
        location8 = Location('test', 5, "culture1", 30, 25,(100, 98))

        self.assertTrue(location7.temp_distance(location8) == 1.0)

    def test_cult_distance(self):
        location1 = Location('test', 0, "Irish", 30, 25,(375,0))
        location2 = Location('test', 11, "American", 30, 25,(100, 0))

        self.assertTrue(location1.cult_distance(location2) == 3.0)

        location3 = Location('test', 1, "Australian", 30, 25,(100, 100))
        location4 = Location('test', 9, "Canadian", 30, 25,(100, 0))

        self.assertTrue(location3.cult_distance(location4) == 2.0)

        location5 = Location('test', 4, "Brazilian", 30, 25,(100, 100))
        location6 = Location('test', 9, "Indian", 30, 25,(93, 90))

        self.assertTrue(location5.cult_distance(location6) == 16.0)

        location7 = Location('test', 2, "Indian", 30, 25,(100, 100))
        location8 = Location('test', 5, "Japanese", 30, 25,(100, 98))

        self.assertTrue(location7.cult_distance(location8) == 13.0)

    def test_dist_g(self):
        location1 = Location('test', 0, "Irish", 30, 25,(375,0))
        location2 = Location('test', 11, "American", 30, 25,(100, 0))

        self.assertTrue(location1.dist_g(location2) == 11.0)

        location3 = Location('test', 1, "Australian", 30, 25,(100, 100))
        location4 = Location('test', 9, "Canadian", 30, 25,(100, 0))

        self.assertTrue(location3.dist_g(location4) == 8.0)

        location5 = Location('test', 4, "Brazilian", 30, 25,(100, 100))
        location6 = Location('test', 9, "Indian", 30, 25,(93, 90))

        self.assertTrue(location5.dist_g(location6) == 20.0)

        location7 = Location('test', 2, "Indian", 30, 25,(100, 100))
        location8 = Location('test', 5, "Japanese", 30, 25,(100, 98))

        self.assertTrue(location7.dist_g(location8) == 15.0)

        self.assertTrue(location7.dist_g(location7) == 2.0)

    def test_calc_fail(self):
        # This test will only make sure that calc_fail will return a bool
        # We cannot verify anything else since there is a random element involved
        location1 = Location('test', 0, "Irish", 30, 25,(375,0))
        location2 = Location('test', 11, "American", 30, 25,(100, 0))

        failed = location1.calc_fail(location2)
        self.assertTrue(failed == True or failed == False)

        location3 = Location('test', 1, "Australian", 30, 25,(100, 100))
        location4 = Location('test', 9, "Canadian", 30, 25,(100, 0))

        failed = location3.calc_fail(location4)
        self.assertTrue(failed == True or failed == False)

        location5 = Location('test', 4, "Brazilian", 30, 25,(100, 100))
        location6 = Location('test', 9, "Indian", 30, 25,(93, 90))

        failed = location5.calc_fail(location6)
        self.assertTrue(failed == True or failed == False)

        location7 = Location('test', 2, "Indian", 30, 25,(100, 100))
        location8 = Location('test', 5, "Japanese", 30, 25,(100, 98))

        failed = location7.calc_fail(location8)
        self.assertTrue(failed == True or failed == False)

if __name__ == '__main__':
    unittest.main()
