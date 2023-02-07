import unittest
from src.utilities.types import Parameter, Target, FeatureDefinition
from src.interfaces.analytical_interface import AnalyticalInterface
from src.blocks.optimization import NelderMeadSearch, NSGA_III
from problem_objective import objective_4, objective_3
from pandas import DataFrame
from pymoo.core.population import Population


class TestOptimization(unittest.TestCase):

    p1 = Parameter("p1", 0, 3)
    f1 = Target("f1", 1, ineq=2, is_objective=True, is_constraint=False)
    f2 = Target("f2", 0.5, ineq=2, is_objective=False, is_constraint=True)

    features_1 = FeatureDefinition([p1], [f1, f2])
    features_2 = FeatureDefinition([p1], [f1])

    anal_1 = AnalyticalInterface(objective_4, features_1)
    anal_2 = AnalyticalInterface(objective_3, features_2)

    popsize = 10

    optimization_1 = NSGA_III(anal_1.objective, features_1, popsize)
    optimization_2 = NelderMeadSearch(anal_2.objective, features_2, popsize)

    def test_call(self):
        results_2 = TestOptimization.optimization_2(("n_gen", 1000))
        results_1 = TestOptimization.optimization_1(("n_gen", 200))
        self.assertIsInstance(results_1, dict)
        for key in ["x", "x_hist", "fval_hist", "last_pop"]:
            self.assertIn(key, results_1.keys())
        self.assertIsInstance(results_2["x"], DataFrame)
        self.assertIsInstance(results_1["x"], DataFrame)
        self.assertIsInstance(results_2["x_hist"], DataFrame)
        self.assertIsInstance(results_1["x_hist"], DataFrame)
        self.assertIsInstance(results_2["fval_hist"], DataFrame)
        self.assertIsInstance(results_1["fval_hist"], DataFrame)
        self.assertIsInstance(results_2["last_pop"], Population)
        self.assertIsInstance(results_1["last_pop"], Population)
