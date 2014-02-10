from Problem import Problem

class Task(object):

    def __init__(self, name, cost):
        self.name = name
        self.cost = cost
        self.progress = 0
        self.completed = False
        self.problems = list()

	

