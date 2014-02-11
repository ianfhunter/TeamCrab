from Task import Task

class Module(object):

    def __init__(self, name, cost):
        self.name = name
        self.base_cost = cost
        self.modules = list()
        self.tasks = list()
        #Task init needed

