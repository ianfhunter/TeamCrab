import importme
import unittest
from Module import Module, calculate_actual_cost
from Task import Task
import datetime

class TestModule(unittest.TestCase):

    def setUp(self):
        pass

    def test_constructor(self):
        module = Module('test_module', 600)
        self.assertTrue(module.name == 'test_module' and module.expected_cost == 600 
            and not module.modules and not module.completed_tasks and len(module.tasks) == 7)
        self.assertTrue(module.tasks[0].actual_cost >= int(90*0.75) and module.tasks[0].actual_cost <= int(90*1.25))
        self.assertTrue(module.tasks[1].actual_cost >= int(90*0.75) and module.tasks[1].actual_cost <= int(90*1.25))
        self.assertTrue(module.tasks[2].actual_cost >= int(60*0.75) and module.tasks[2].actual_cost <= int(60*1.25))
        self.assertTrue(module.tasks[3].actual_cost >= int(90*0.75) and module.tasks[3].actual_cost <= int(90*1.25))
        self.assertTrue(module.tasks[4].actual_cost >= int(90*0.75) and module.tasks[4].actual_cost <= int(90*1.25))
        self.assertTrue(module.tasks[5].actual_cost >= int(90*0.75) and module.tasks[5].actual_cost <= int(90*1.25))
        self.assertTrue(module.tasks[6].actual_cost >= int(90*0.75) and module.tasks[6].actual_cost <= int(90*1.25))

    def test_get_task(self):
        module = Module('test_module', 600)

        task = module.get_task('design')
        self.assertTrue(task and task.name == 'design' and task.actual_cost >= int(90*0.75) and task.actual_cost <= int(90*1.25) and task.module == module)

        task = module.get_task('implementation')
        self.assertTrue(task and task.name == 'implementation' and task.actual_cost >= int(90*0.75) and task.actual_cost <= int(90*1.25) and task.module == module)

        task = module.get_task('unit_test')
        self.assertTrue(task and task.name == 'unit_test' and task.actual_cost >= int(60*0.75) and task.actual_cost <= int(60*1.25) and task.module == module)

        task = module.get_task('integration')
        self.assertTrue(task and task.name == 'integration' and task.actual_cost >= int(90*0.75) and task.actual_cost <= int(90*1.25) and task.module == module)

        task = module.get_task('system_test')
        self.assertTrue(task and task.name == 'system_test' and task.actual_cost >= int(90*0.75) and task.actual_cost <= int(90*1.25) and task.module == module)

        task = module.get_task('deployment')
        self.assertTrue(task and task.name == 'deployment' and task.actual_cost >= int(90*0.75) and task.actual_cost <= int(90*1.25) and task.module == module)

        task = module.get_task('acceptance_test')
        self.assertTrue(task and task.name == 'acceptance_test' and task.actual_cost >= int(90*0.75) and task.actual_cost <= int(90*1.25) and task.module == module)

        task = module.get_task('not_a_task')
        self.assertTrue(not task)

    def test_calculate_actual_cost(self):
        for i in range(100, 150):
            val = calculate_actual_cost(i,25)
            print i, val
            self.assertTrue(val >= i*0.75 and val <= i*1.25)

    def test_progress_module(self):
        module = Module('test_module', 600)
        current_time = datetime.datetime(2014,1,1,0,0,0)
        module.calc_deadline(current_time, 10, 0)

        for i in range(60):
            current_time += datetime.timedelta(hours=1)
            module.progress_module(10, current_time)

        self.assertTrue(module.progress >= 500 or module.progress <= 700)

    def test_calc_deadline(self):
        module = Module('test_module', 600)
        start_time = datetime.datetime(2014,1,1,0,0,0)
        deadline = datetime.datetime(2014,1,22,0,0,0)

        module.calc_deadline(start_time, 10, 0)
        print module.deadline
        self.assertTrue(module.deadline == deadline)

        module.calc_deadline(start_time, 600, 0)
        self.assertTrue(module.deadline == start_time)

    def test_wall_clock_time(self):
        module = Module('test_module', 600)
        
        self.assertTrue(module.wall_clock_time() == 0)
        module.total_hours += 10
        self.assertTrue(module.wall_clock_time() == 10)

    def test_productive_time_on_task(self):
        module = Module('test_module', 600)
        
        self.assertTrue(module.productive_time_on_task() == 0)
        module.hours_taken += 10
        self.assertTrue(module.productive_time_on_task() == 10)

if __name__ == '__main__':
    unittest.main()
