import unittest
from src.utilities.types import Parameter


class TestParameter(unittest.TestCase):

    p1 = Parameter("p1", 0, 1)

    def test_state(self):
        self.assertEqual(TestParameter.p1.name, "p1")
        self.assertEqual(TestParameter.p1.lb, 0)
        self.assertEqual(TestParameter.p1.ub, 1)
        self.assertIsInstance(TestParameter.p1.lb, float)
        self.assertIsInstance(TestParameter.p1.ub, float)

    def test_repr(self):
        self.assertEqual(TestParameter.p1.__repr__(), "Parameter('p1', 0.0, 1.0)")
