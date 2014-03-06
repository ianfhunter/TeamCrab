from Task import Task


class Module(object):
    def __init__(self, name, cost):
        self.name = name
        self.cost = cost
        self.modules = list()
        self.tasks = list()
        self.completed_tasks = list()

        self.tasks.append(Task('design', self.cost/100*15, self))
        self.tasks.append(Task('implementation', self.cost/100*15, self))
        self.tasks.append(Task('unit_test', self.cost/100*10, self))
        self.tasks.append(Task('integration', self.cost/100*15, self))
        self.tasks.append(Task('system_test', self.cost/100*15, self))
        self.tasks.append(Task('deployment', self.cost/100*15, self))
        self.tasks.append(Task('acceptance_test', self.cost/100*15, self))

        self.progress = 0.0
        self.expected_progress = 0.0
        self.completed = False
        self.stalled = False
        self.hours_taken = 0 # This is productive time
        self.total_hours = 0 # number of hours from start of project including non productive hours. 

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
        return self.progress >= self.expected_progress - (self.expected_progress/4)
