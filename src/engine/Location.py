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
        if team.size + self.current_size > self.capacity:
            return False
        else:
            self.current_size += team.size
            self.teams.append(team)
            return True

    def calc_mod(self):
        return cultures[self.culture][0]

    def num_teams(self):
        return len(self.teams)

    def average_efficiency(self):
        total = 0.0
        for team in self.teams:
            total += team.efficiency*cultures[self.culture][0]
        return int(total/len(self.teams) * 100)

    def total_task_progress(self):
        total = 0
        for team in self.teams:
            total += team.task.progress
        return total

    def num_tasks_on_schedule(self):
        total = 0
        for team in self.teams:
            if team.task.is_on_time():
                total += 1
        return total
