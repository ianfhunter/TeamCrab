import importme
import unittest
from Location import Location
from Culture import Culture
from Team import Team

class TestLocation(unittest.TestCase):

    def setUp(self):
        pass

    def test_constructor(self):
        culture = Culture('Ireland', 0.8, 0.7)
        location = Location('Dublin', 0, culture, 30, 25,(375,148))
        self.assertTrue(location.name == 'Dublin' and location.time_zone == 0 and location.culture == culture
            and location.capacity == 30 and location.salary == 25 and not location.teams and not location.specialists)

    def test_add_team(self):
        culture = Culture('Ireland', 0.8, 0.7)
        location = Location('Dublin', 0, culture, 30, 25,(375,148))

        team1 = Team('test_team1', 0.9, 25, 10)
        self.assertTrue(location.add_team(team1))

        team2 = Team('test_team2', 0.6, 20, 20)
        self.assertTrue(location.add_team(team2))

        team3 = Team('test_team3', 0.5, 20, 1)
        self.assertFalse(location.add_team(team3))

        self.assertTrue(len(location.teams) == 2)

    def test_calc_mod(self):
        culture = Culture('Ireland', 0.8, 0.7)
        location = Location('Dublin', 0, culture, 30, 25,(375,148))

        self.assertTrue(location.calc_mod() == 0.8)

if __name__ == '__main__':
    unittest.main()
