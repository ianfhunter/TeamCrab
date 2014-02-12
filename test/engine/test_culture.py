import importme
import unittest
from Culture import Culture

class TestCulture(unittest.TestCase):

    def setUp(self):
        pass

    def test_constructor(self):
        culture = Culture('Ireland', 0.8, 0.9)
        self.assertTrue(culture.name == 'Ireland' and culture.efficiency_mod == 0.8 and culture.honesty_at == 0.9)

if __name__ == '__main__':
    unittest.main()
