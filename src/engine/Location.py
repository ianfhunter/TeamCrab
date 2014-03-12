from Team import Team
from global_config import cultures, config, global_distance
import random
import math

class Location(object):

    def __init__(self, name, time, culture, cap, cost, coordinates):
        self.name = name
        self.time_zone = time
        self.culture = culture
        self.capacity = cap
        self.current_size = 0
        self.teams = list()
        self.salary = cost
        self.specialists = list()
        self.coordinates = coordinates

    def add_team(self, team):
        ''' Adds a team to this location if there is enough space for them.
        Returns true if the team was added, false otherwise.
        '''
        if team.size + self.current_size > self.capacity:
            return False
        else:
            self.current_size += team.size
            self.teams.append(team)
            return True


    def num_teams(self):
        ''' Returns the number of teams at this location.
        '''
        return len(self.teams)

    def total_module_progress(self):
        ''' Returns the total progress of all modules assigned to teams in this location.
        '''
        total = 0
        for team in self.teams:
            if team.module:    #check
                total += team.module.progress
        return total

    def num_modules_on_schedule(self):
        ''' Returns the number of modules being performed by teams at this location that are "on time".
        '''
        total = 0
        for team in self.teams:
            if team.module: 
                if team.module.is_on_time:
                    total += 1
        return total

    def num_modules(self):
        total = 0
        for team in self.teams:
            if team.module: 
                total += 1
        return total

    def geo_distance(self, loc):
        #TODO these distances are made up and need to be adjusted based on map scale
        distance = math.sqrt(math.pow(self.coordinates[0] - loc.coordinates[0], 2)+math.pow(self.coordinates[1] - loc.coordinates[1], 2))
        if distance >= 200:
            return global_distance["high"]
        if distance >= 50:
            return global_distance["medium_high"]
        if distance >= 10:
            return global_distance["medium_low"]
        return global_distance["low"]

    def temp_distance(self, loc):
        temporal = abs(self.time_zone - loc.time_zone)
        if temporal > 12:
            temporal = 24 - temporal
        if temporal <= 3:
            return global_distance["low"]
        if temporal <= 5:
            return global_distance["medium_low"]
        if temporal <= 8:
            return global_distance["medium_high"]
        return global_distance["high"]

    def cult_distance(self, loc):
        culture = 0.0
        if cultures[self.culture][1] != cultures[loc.culture][1]:
            culture += global_distance["high"]
        if cultures[self.culture][2] != cultures[loc.culture][2]:
            culture += global_distance["medium_high"]
        if cultures[self.culture][3] != cultures[loc.culture][3]:
            culture += global_distance["medium_high"]
        if cultures[self.culture][4] != cultures[loc.culture][4]:
            culture += global_distance["medium_high"]
        if cultures[self.culture][5] != cultures[loc.culture][5]:
            culture += global_distance["medium_low"]
        if cultures[self.culture][6] != cultures[loc.culture][6]:
            culture += global_distance["low"]
        return culture

    def dist_g(self, loc):
        return self.geo_distance(loc) + self.temp_distance(loc) + self.cult_distance(loc)

    def calc_fail(self, loc):
        d_glo = self.dist_g(loc)
        p_fail = config["fail_rate"] * (d_glo / (1 + d_glo))
        if random.random() <= p_fail:
            return True
        return False

