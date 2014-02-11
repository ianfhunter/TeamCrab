
class Team(object):

    def __init__(self, name, effiency, salary, size):
        self.name = name
        self.salary = salary
        self.effiency = effiency
        self.size = size
        self.task = None

    def calc_progress(self, mod):
        if not self.task.completed:
            self.task.progress += self.effiency * mod
            if self.task.progress >= self.task.cost:
                print self.name + '\'s task has completed!'
                self.task.module.completed_tasks.append(self.task.module.tasks.pop())
                self.task.completed = True
        

