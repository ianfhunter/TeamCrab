import importme
import unittest
from Module import Module
from Task import Task

class TestModule(unittest.TestCase):

    def setUp(self):
        pass

    def test_constructor(self):
        module = Module('test_module', 600)
        self.assertTrue(module.name == 'test_module' and module.base_cost == 600 
            and not module.modules and not module.completed_tasks and len(module.tasks) == 7)
        self.assertTrue(module.tasks[0].cost == 90)
        self.assertTrue(module.tasks[1].cost == 90)
        self.assertTrue(module.tasks[2].cost == 60)
        self.assertTrue(module.tasks[3].cost == 90)
        self.assertTrue(module.tasks[4].cost == 90)
        self.assertTrue(module.tasks[5].cost == 90)
        self.assertTrue(module.tasks[6].cost == 90)

    def test_get_task(self):
        module = Module('test_module', 600)

        task = module.get_task('design')
        self.assertTrue(task and task.name == 'design' and task.cost == 90 and task.module == module)

        task = module.get_task('implementation')
        self.assertTrue(task and task.name == 'implementation' and task.cost == 90 and task.module == module)

        task = module.get_task('unit_test')
        self.assertTrue(task and task.name == 'unit_test' and task.cost == 60 and task.module == module)

        task = module.get_task('integration')
        self.assertTrue(task and task.name == 'integration' and task.cost == 90 and task.module == module)

        task = module.get_task('system_test')
        self.assertTrue(task and task.name == 'system_test' and task.cost == 90 and task.module == module)

        task = module.get_task('deployment')
        self.assertTrue(task and task.name == 'deployment' and task.cost == 90 and task.module == module)

        task = module.get_task('acceptance_test')
        self.assertTrue(task and task.name == 'acceptance_test' and task.cost == 90 and task.module == module)

        task = module.get_task('not_a_task')
        self.assertTrue(not task)

if __name__ == '__main__':
    unittest.main()