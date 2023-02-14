import unittest

from src.blocks.data import Data
from src.blocks.surrogates import Polynomial
from src.interfaces.analytical_interface import AnalyticalInterface
from src.utilities.types import FeatureDefinition, Parameter, Target
from numpy.random import randint
from pandas import DataFrame

from problem_objective import objective_5


class TestData(unittest.TestCase):
    x1 = Parameter("x1", 0, 2)
    f1 = Target("f1", 0.5, ineq=5, is_objective=True, is_constraint=True)
    f2 = Target("f2", 0.5, ineq=5, is_objective=False, is_constraint=True)
    f3 = Target("f3", 0.5, ineq=5, is_objective=False, is_constraint=True)

    features = FeatureDefinition([x1], [f1, f2, f3])

    a_int = AnalyticalInterface(objective_5, features).objective
    data = []
    for x in randint(-10, 10, size=(20, 1)):
        f = a_int(x)
        data.append([*x, *f])
    data_ok = DataFrame(data, columns=["x1", "f1", "f2", "f3"])
    samples = DataFrame([[1], [1], [2]], columns=["x1"])

    def test_state(self):
        pass

    def test_add(self):
        sur_5, _ = Polynomial(1, True, False)(TestData.data_ok, TestData.features)
        colldata = Data(TestData.features, sur_5)
        colldata_added = colldata.add(TestData.data_ok, samples=TestData.samples)
        self.assertEqual(colldata_added["x1"].iloc[-1], 2)
        self.assertEqual(colldata_added.shape[0], 23)
