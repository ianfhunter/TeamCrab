from Problem import Problem


class Task(object):
    def __init__(self, name, cost, module):
        self.name = name
        self.cost = cost
        self.progress = 0.0
        self.expected_progress = 0.0
        self.completed = False
        self.problems = list()
        self.module = module
        self.stalled = False


    def is_on_time(self):
        return self.progress >= self.expected_progress
