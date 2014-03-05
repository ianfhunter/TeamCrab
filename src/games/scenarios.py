import toolchain
import traffic_monitor

def get_scenarios():
	scenarios = dict()
	scenarios[toolchain.get_name()] = toolchain.load_game()
	scenarios[traffic_monitor.get_name()] = traffic_monitor.load_game()
	return scenarios
