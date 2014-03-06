import toolchain
import traffic_monitor
import web_ap

def get_scenarios():
	scenarios = dict()
	scenarios[toolchain.get_name()] = toolchain.load_game()
	scenarios[traffic_monitor.get_name()] = traffic_monitor.load_game()
	scenarios[web_ap.get_name()] = web_ap.load_game()
	return scenarios
