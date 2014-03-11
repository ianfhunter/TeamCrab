import importme
import unittest
from Module import Module, calculate_actual_cost
from Task import Task

class TestModule(unittest.TestCase):

    def setUp(self):
        pass

    def test_constructor(self):
        module = Module('test_module', 600)
        self.assertTrue(module.name == 'test_module' and module.expected_cost == 600 
            and not module.modules and not module.completed_tasks and len(module.tasks) == 7)
        self.assertTrue(module.tasks[0].cost >= 90*0.75 and module.tasks[0].cost <= 90*1.25)
        self.assertTrue(module.tasks[1].cost >= 90*0.75 and module.tasks[1].cost <= 90*1.25)
        self.assertTrue(module.tasks[2].cost >= 60*0.75 and module.tasks[2].cost <= 60*1.25)
        self.assertTrue(module.tasks[3].cost >= 90*0.75 and module.tasks[3].cost <= 90*1.25)
        self.assertTrue(module.tasks[4].cost >= 90*0.75 and module.tasks[4].cost <= 90*1.25)
        self.assertTrue(module.tasks[5].cost >= 90*0.75 and module.tasks[5].cost <= 90*1.25)
        self.assertTrue(module.tasks[6].cost >= 90*0.75 and module.tasks[6].cost <= 90*1.25)

    def test_get_task(self):
        module = Module('test_module', 600)

        task = module.get_task('design')
        self.assertTrue(task and task.name == 'design' and task.cost >= 90*0.75 and task.cost <= 90*1.25 and task.module == module)

        task = module.get_task('implementation')
        self.assertTrue(task and task.name == 'implementation' and task.cost >= 90*0.75 and task.cost <= 90*1.25 and task.module == module)

        task = module.get_task('unit_test')
        self.assertTrue(task and task.name == 'unit_test' and task.cost >= 60*0.75 and task.cost <= 60*1.25 and task.module == module)

        task = module.get_task('integration')
        self.assertTrue(task and task.name == 'integration' and task.cost >= 90*0.75 and task.cost <= 90*1.25 and task.module == module)

        task = module.get_task('system_test')
        self.assertTrue(task and task.name == 'system_test' and task.cost >= 90*0.75 and task.cost <= 90*1.25 and task.module == module)

        task = module.get_task('deployment')
        self.assertTrue(task and task.name == 'deployment' and task.cost >= 90*0.75 and task.cost <= 90*1.25 and task.module == module)

        task = module.get_task('acceptance_test')
        self.assertTrue(task and task.name == 'acceptance_test' and task.cost >= 90*0.75 and task.cost <= 90*1.25 and task.module == module)

        task = module.get_task('not_a_task')
        self.assertTrue(not task)

    def test_random_element(self):
        for i in range(100, 150):
            val = calculate_actual_cost(i)
            print i, val
            self.assertTrue(val >= i*0.75 and val <= i*1.25)

    def test_expected_cost(self):
        module1 = Module('test_module', 600)
        self.assertTrue(module1.expected_cost == 600)

        module2 = Module('test_module', 400)
        self.assertTrue(module2.expected_cost == 400)

        module3 = Module('test_module', 0)
        self.assertTrue(module3.expected_cost == 0)

if __name__ == '__main__':
    unittest.main()
