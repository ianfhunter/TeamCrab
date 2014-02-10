
class Team(object):

    def __init__(self, name, effiency, salary, size):
        self.name = name
        self.salary = salary
        self.effiency = effiency
        self.size = size
        self.task = None

    def calc_progress(self, mod):
        self.task.progress += self.effiency * mod
        if self.task.progress >= self.task.cost:
            self.task.completed = True
        

