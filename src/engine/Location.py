from Team import Team
from Culture import Culture

class Location(object):

    def __init__(self, name, time, culture, cap, cost):
        self.name = name
        self.time_zone = time
        self.culture = culture
        self.capacity = cap
        self.teams = list()
        self.salery = cost
        self.specialists = list()

    def add_team(self,team):
        self.teams.append(team)

    def calc_mod(self):
        return self.culture.efficiency_mod
	


	
