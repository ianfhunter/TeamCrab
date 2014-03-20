import csv
import json
import copy
from global_config import config 
import math

def total_person_hours(project):
    '''
    Calculates the total estimated and actual person hours of effort expended in a project `project'.
    '''
    total_estimated = project.expected_budget() / config["developer_hourly_cost"]
    total_actual = project.actual_budget() / config["developer_hourly_cost"]
    return (int(total_estimated), int(total_actual))

def report_table_line(team, module, size, estimate, actual, cost, wall, productive):
    '''
    Formats a line of the endgame report dump.
    '''
    s = ""
    s += team + (" " * (15 - (len(team))))
    s += module + (" " * (13 - len(module)))
    s += str(size) + (" " * (6 - (len(str(size)))))
    s += str(estimate) + (" " * (16 - (len(str(estimate)))))
    s += str(actual) + (" " * (15 - (len(str(actual)))))
    s += str(cost) + (" " * (10 - (len(str(cost)))))
    s += str(wall) + (" " * (13 - len(str(wall))))
    s += str(productive)
    return s

def generate_report(project):
    '''
    Generates endgame report for the project `project'.
    '''
    report = {}
    report["score"] = project.game_score()
    report["total_time"] = str(project.current_time - project.start_time)
    report["nominal_end_time"] = str(project.delivery_date)
    report["actual_end_time"] = str(project.current_time)
    report["days_behind_schedule"] = project.days_behind_schedule()
    report["expected_budget"] = project.expected_budget()
    report["actual_budget"] = project.actual_budget()
    report["expected_revenue"] = project.expected_revenue()
    report["actual_revenue"] = project.actual_revenue()
    report["endgame_cash"] = project.game_score()

    # Generate table to compare estimated/actual effort broken down by module
    effort_table = []
    effort_table.append(['Team', 'Module', 'Team', 'Expected Effort', 'Actual Effort  ', 'Module', 'Wall clock', 'Staff Time'])
    effort_table.append(['Name', 'Name',   'Size', '(man hrs)',       '(man hrs)  ',     'Cost $', 'time (hrs)', 'time (hrs)'])
    total_estimated = 0
    total_actual = 0
    for location in project.locations:
        for team in location.teams:
            for module in team.completed_modules:
                expected = int(module.expected_cost)
                actual = int(module.actual_cost)
                wall = module.wall_clock_time()
                productive = module.productive_time_on_task() * team.size
                dollars = int(productive * config["developer_hourly_cost"] )
                effort_table.append([team.name, module.name, team.size, expected, actual, dollars, wall, productive])
                total_estimated += expected
                total_actual += actual
    # Add totals row
    # effort_table.append(["Total", "Total", total_estimated, total_actual])
    
    report["effort_table"] = effort_table
    
    return report

def write_endgame_json(report):
    '''
    Writes the endgame report, given a report `report'
    
    @untestable - This function is just a call to the python standard library and thus makes no sense to test.
    '''
    end_report = copy.deepcopy(report)
    table = end_report["effort_table"]
    del end_report["effort_table"]
    outfile = open('report.txt', 'w')
    outfile.write(json.dumps(end_report, indent=4))
    outfile.write('\n')

    writer = csv.writer(outfile, delimiter=',')
    writer.writerows(table)


