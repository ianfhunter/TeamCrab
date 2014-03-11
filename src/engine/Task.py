from Problem import Problem


class Task(object):
    def __init__(self, name, actual_cost, expected_cost, module):
        self.name = name
        self.expected_cost = expected_cost
        self.actual_cost = actual_cost
        self.deadline = None
        self.completed = False
        self.problems = list()
        self.module = module
        self.stalled = False
        self.hours_taken = 0
