'''
A class that represents an intervention for a problem in the simulator.
'''
class Intervention(object):
    def __init__(self, name, impact, cost):
        self.name = name

        if cost == "High":
            self.cost = 4
        elif cost == "Med High":
            self.cost = 3
        elif cost == "Med Low":
            self.cost = 2
        elif cost == "Low":
            self.cost = 1
        else:
            self.cost = 0

        if impact == "High":
            self.impact = 4
        elif impact == "Med High":
            self.impact = 3
        elif impact == "Med Low":
            self.impact = 2
        elif impact == "Low":
            self.impact = 1
        else:
            self.impact = 0

    def get_cost(self):
        '''
        Returns the cost of this intervention in terms of cash
        '''
        if self.cost == 1:
            return 5000
        if self.cost == 2:
            return 25000
        if self.cost == 3:
            return 125000
        if self.cost == 4:
            return 500000
        else :
            return 0   