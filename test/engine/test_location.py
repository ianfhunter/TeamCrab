import importme
import unittest
from Location import Location
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


if __name__ == '__main__':
    unittest.main()
