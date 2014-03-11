import random
from Task import Task
from global_config import problems

def random_element(prog):
    ''' Generates a random value between -25 and 25 used as a percentage to offset prog.
    '''
    amount = float(random.randint(-25, 25))
    direction = random.choice([-1, 1])
    return prog * (1 + (amount / 100.0))

class Module(object):
    def __init__(self, name, cost):
        self.name = name
        self.expected_cost = cost
        self.actual_cost = random_element(cost)
        self.actual_cost_base = self.actual_cost
        self.modules = list()
        self.tasks = list()
        self.completed_tasks = list()

        self.tasks.append(Task('design', self.actual_cost/100*15, self))
        self.tasks.append(Task('implementation', self.actual_cost/100*15, self))
        self.tasks.append(Task('unit_test', self.actual_cost/100*10, self))
        self.tasks.append(Task('integration', self.actual_cost/100*15, self))
        self.tasks.append(Task('system_test', self.actual_cost/100*15, self))
        self.tasks.append(Task('deployment', self.actual_cost/100*15, self))
        self.tasks.append(Task('acceptance_test', self.actual_cost/100*15, self))

        self.progress = 0.0
        self.completed = False
        self.stalled = False
        self.hours_taken = 0 # This is productive time
        self.total_hours = 0 # number of hours from start of project including non productive hours. 
        self.problems_occured = list()

    # TODO: Consider changing tasks to be a dictionary for O(1) lookups
    # by name.
    # Doing a linear search through the list here will be slow and a dict
    # would be preferable.

    # Reason for list is so task have to be performed in order. 
    def get_task(self, name):
        ''' Returns the task object which matches the name specified if it exists, None otherwise.
        '''
        tasks = [task for task in self.tasks if task.name == name]
        if tasks:
            return tasks[0]
        else:
            return None

    def is_on_time(self):
        ''' Returns True if the progress of this task is at least equal to 75% of the expected progress,
        False otherwise
        '''
        return self.progress < (self.actual_cost * .75)

    def expected_cost(self):
        return self.expected_cost

    def actual_cost(self):
        return self.actual_cost

    def wall_clock_time(self):
        return self.total_hours

    def productive_time_on_task(self):
        return self.hours_taken

    def add_problem(self):
        prob = random.randint(1, 5)
        self.problems_occured.append(problems[prob][0])
        self.actual_cost += self.actual_cost_base * problems[prob][1]

