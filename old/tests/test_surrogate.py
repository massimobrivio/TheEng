from typing import Iterable
import unittest
from src.blocks.surrogates import Polynomial
from src.utilities.types import Parameter, Target, FeatureDefinition
from pandas import DataFrame
from numpy.random import randint


class TestSurrogate(unittest.TestCase):
    data = DataFrame(randint(-10, 10, size=(20, 4)), columns=["x1", "f1", "f2", "f3"])
    x1 = Parameter("x1", 0, 2)
    f1 = Target("f1", 0.5, ineq=5, is_objective=True, is_constraint=True)
    f2 = Target("f2", 0.5, ineq=5, is_objective=False, is_constraint=True)
    f3 = Target("f3", 0.5, ineq=5, is_objective=False, is_constraint=False)
    features = FeatureDefinition([x1], [f1, f2, f3])
    poly = Polynomial(1, True, False)

    def test_call(self):
        sur, performance = TestSurrogate.poly(
            TestSurrogate.data, TestSurrogate.features
        )
        self.assertIsInstance(performance, tuple)
        self.assertLessEqual(performance[0], 1.0)
        self.assertIsInstance(sur([2]), Iterable)
        self.assertIsInstance(sur([2])[0], float)
