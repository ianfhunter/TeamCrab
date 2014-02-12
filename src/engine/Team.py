
class Team(object):

    def __init__(self, name, effiency, salary, size):
        self.name = name
        self.salary = salary
        self.efficiency = effiency
        self.size = size
        self.task = None

    def calc_progress(self, mod):
        if not self.task.completed:
            self.task.progress += self.efficiency * mod
            if self.task.progress >= self.task.cost:
                print self.name + '\'s task has completed!'
                self.task.module.completed_tasks.append(self.task)
                self.task.module.tasks.remove(self.task)
                self.task.completed = True
        

