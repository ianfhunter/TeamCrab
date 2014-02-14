from Team import Team
from Culture import Culture

class Location(object):

    def __init__(self, name, time, culture, cap, cost,coordinates):
        self.name = name
        self.time_zone = time
        self.culture = culture
        self.capacity = cap
        self.current_size = 0
        self.teams = list()
        self.salary = cost
        self.specialists = list()
        self.coordinates = coordinates

    def add_team(self,team):
        if team.size + self.current_size > self.capacity:
            return False
        else:
            self.current_size += team.size
            self.teams.append(team)
            return True

    def calc_mod(self):
        return self.culture.efficiency_mod
	


	
