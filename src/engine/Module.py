from Task import Task

class Module(object):

    def __init__(self, name, cost):
        self.name = name
        self.base_cost = cost
        self.modules = list()
        self.tasks = list()

        self.tasks.append(Task('design', self.base_cost/100*15))
        self.tasks.append(Task('implementation', self.base_cost/100*15))
        self.tasks.append(Task('unit_test', self.base_cost/100*10))
        self.tasks.append(Task('integration', self.base_cost/100*15))
        self.tasks.append(Task('system_test', self.base_cost/100*15))
        self.tasks.append(Task('deployment', self.base_cost/100*15))
        self.tasks.append(Task('acceptance_test ', self.base_cost/100*15))


