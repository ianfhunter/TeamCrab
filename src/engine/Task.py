from Problem import Problem

class Task(object):
    '''
    Represents a task, a sub-part of a Module (as described in the backlog).
    '''
    def __init__(self, name, actual_cost, expected_cost, module):
        self.name = name
        self.expected_cost = expected_cost
        self.actual_cost = actual_cost
        self.original_actual_cost = actual_cost
        self.deadline = None
        self.completed = False
        self.problems = list()
        self.module = module
        self.stalled = False
        self.hours_taken = 0

    def current_cost(self):
        '''
        Returns the current actual cost of this task. This value may change if there are
        problems added to the parent module of this task.
        '''
        return self.actual_cost

    def increase_cost(self, person_hours):
        '''
        Increase the actual cost of this task by the amount specified by person_hours
        '''
        self.actual_cost += person_hours
