from Task import Task


class Module(object):
    def __init__(self, name, cost):
        self.name = name
        self.base_cost = cost
        self.modules = list()
        self.tasks = list()
        self.completed_tasks = list()

        self.tasks.append(Task('design', self.base_cost/100*15, self))
        self.tasks.append(Task('implementation', self.base_cost/100*15, self))
        self.tasks.append(Task('unit_test', self.base_cost/100*10, self))
        self.tasks.append(Task('integration', self.base_cost/100*15, self))
        self.tasks.append(Task('system_test', self.base_cost/100*15, self))
        self.tasks.append(Task('deployment', self.base_cost/100*15, self))
        self.tasks.append(Task('acceptance_test', self.base_cost/100*15, self))

    # TODO: Consider changing tasks to be a dictionary for O(1) lookups
    # by name.
    # Doing a linear search through the list here will be slow and a dict
    # would be preferable.
    def get_task(self, name):
        tasks = [task for task in self.tasks if task.name == name]
        if tasks:
            return tasks[0]
        else:
            return None
