from Team import Team
from global_config import cultures, config, global_distance
import random
import math

locations_information = dict()
locations_information['Dublin'] = {"coords" : (375,148), "timezone" : 0}
locations_information['Belarus'] = {"coords" : (445,138), "timezone" : 3}
locations_information['Rio de Janeiro'] = {"coords" : (285,337), "timezone" : -3}
locations_information['Florida'] = {"coords" : (192,207), "timezone" : -5}
locations_information['Toronto'] = {"coords" : (206,179), "timezone" : -5}
locations_information['Canberra'] = {"coords" : (733,369), "timezone" : 11}
locations_information['Tokyo'] = {"coords" : (704,201), "timezone" : 9}
locations_information['Nuuk'] = {"coords" : (273,68), "timezone" : -2}
locations_information['New Dehli'] = {"coords" : (570,264), "timezone" : 5}

class Location(object):
    '''
    A class representing a location in the simulator.
    '''

    def __init__(self, name, culture, cap):
        self.name = name
        self.time_zone = locations_information[name]["timezone"]
        self.culture = culture
        self.capacity = cap
        self.current_size = 0
        self.teams = list()
        self.specialists = list()
        self.coordinates = locations_information[name]["coords"]
        self.fail_rate = config["fail_rate"]
        self.intervention_level = 0

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
        '''
        Returns the number of active modules in this location.
        '''
        total = 0
        for team in self.teams:
            if team.module: 
                total += 1
        return total

    def geo_distance(self, loc):
        '''
        Calculates geographic distance between a site and the home location.
        '''
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
        '''
        Returns the temporal distance between a location and the home location.
        '''
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
        '''
        Returns the cultural distance between a location and the home location.
        '''
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
        '''
        Global distance: the sum of the geographical, temporal and cultural difference between a location and the home site.
        '''
        return self.geo_distance(loc) + self.temp_distance(loc) + self.cult_distance(loc)

    def calc_fail(self, loc):
        '''
        Returns whether one communication between the home site and a location will fail based on "global distance".
        '''
        d_glo = self.dist_g(loc)
        intervention_mod = self.intervention_level / 1 + self.intervention_level
        p_fail = self.fail_rate * (d_glo / (1 + d_glo)) * intervention_mod

        if random.random() <= p_fail:
            return True
        return False

    def add_intervention(self, intervention_type):
        ''' 
            Adds an intervention to a site, meaning problem rates are lowered
            
            Intervention Costs are subtracted from Current Cash.
            Intervention Impact is added to intervention_level which increases the intervention_modifier when caclulating failures.

            Lvl  Name        Cost       Impact
            0    None        $0         +0
            1    Low         $5,000     +1
            2    Med Low     $25,000    +2
            3    Med High    $125,000   +3
            4    High        $500,000   +4

            TODO: Add tests.
        '''
        cost = 0
        impact = 0

        #GEO INTERVENTIONS
        if intervention_type == "Exchange Program":
            #High,         Medium High
            cost = 4
            impact = 3
        elif intervention_type == "Synchronous Communication Possibilities":
            #Med High,     Low
            cost = 3
            impact = 1
        elif intervention_type == "Support for Video Conference":
            #Med Low,      Low
            cost = 2
            impact = 1
        elif intervention_type == "Suitable select of Communication Tools":
            #Med Low,      Low
            cost = 2
            impact = 1

        #TIME INTERVENTIONS
        elif intervention_type == "Relocate to Adjacent Time Zone":
            #High,         High
            cost = 4
            impact = 4
        elif intervention_type == "Adopt Follow The Sun Development":
            #Med High,     High
            cost = 3
            impact = 4
        elif intervention_type == "Create Bridging Team":
            #Med High,     Med High
            cost = 3
            impact = 3

        #CULTURE INTERVENTIONS
        elif intervention_type == "Face to Face Meeting":
            #High,         Med Low
            cost = 4
            impact = 2
        elif intervention_type == "Cultural Training":
            #Med High,     Med Low
            cost = 3
            impact = 2
        elif intervention_type == "Cultural Liason/Ambassador":
            #Med High,     Med High
            cost = 3
            impact = 3
        elif intervention_type == "Adopt low-context communication style":
            #Low,         Low
            cost = 1
            impact = 1
        elif intervention_type == "Reduce interaction between teams":
            #Low,         Low
            cost = 1
            impact = 1

        self.intervention_level += impact
        