'''
From e-mail "[CS4098] Iteration 2 post-mortem (please read carefully)":
'''
class RevenueTier:
    def expected_yearly_profits(self):
        raise NotImplementedError("Abstract base class, not implemented")
        pass

class LowRevenueTier(RevenueTier):
    def expected_yearly_profits(self):
        return 1000000

class MediumRevenueTier(RevenueTier):
    def expected_yearly_profits(self):
        return 5000000

class HighRevenueTier(RevenueTier):
    def expected_yearly_profits(self):
        return 20000000

