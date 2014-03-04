from Team import Team
from global_config import cultures

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

    def calc_mod(self):
        ''' Returns the efficiency modification for this location's culture.
        '''
        return cultures[self.culture][0]

    def num_teams(self):
        ''' Returns the number of teams at this location.
        '''
        return len(self.teams)

    def average_efficiency(self):
        ''' Returns the average efficiency of all teams at this location.
        The result is returned as an integer value and may be prone to rounding errors.
        '''
        total = 0.0
        for team in self.teams:
            total += team.efficiency*cultures[self.culture][0]
        return int(total/len(self.teams) * 100)

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
                if team.module.is_on_time():
                    total += 1
        return total

    def num_modules(self):
        total = 0
        for team in self.teams:
            if team.module: 
                total += 1
        return total

