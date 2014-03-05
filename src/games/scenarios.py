from toolchain import Scenario_Toolchain
from traffic_monitor import Scenario_Traffic_Monitor

def get_scenarios():
	scenarios = list()
	scenarios.append(Scenario_Toolchain())
	scenarios.append(Scenario_Traffic_Monitor())
	return scenarios
