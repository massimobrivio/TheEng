import unittest

from src.utilities.types import Problem, Parameter, Target, FeatureDefinition
from src.interfaces.analytical_interface import AnalyticalInterface
from numpy import array, subtract

from problem_objective import objective_1, objective_2, objective_3


class TestProblem(unittest.TestCase):

    x1 = Parameter("x1", -2.0, 2.0)
    x2 = Parameter("x2", -2.0, 2.0)
    f1 = Target("f1", 0.5, ineq=5.0, is_objective=True, is_constraint=True)
    f2 = Target("f2", 0.5, ineq=2000.0, is_objective=True, is_constraint=True)
    f3 = Target("f1", 0.5, ineq=2000.0, is_objective=True, is_constraint=False)
    f4 = Target("f1", 0.5, ineq=3.0, is_objective=True, is_constraint=True)

    features_1 = FeatureDefinition([x1, x2], [f1, f2])
    features_3 = FeatureDefinition([x1, x2], [f3])
    features_4 = FeatureDefinition([x1], [f4])

    anal_1 = AnalyticalInterface(objective_1, features_1).objective
    anal_3 = AnalyticalInterface(objective_2, features_3).objective
    anal_4 = AnalyticalInterface(objective_3, features_4).objective

    problem_1 = Problem(objective=anal_1, features=features_1)

    problem_3 = Problem(objective=anal_3, features=features_3)

    problem_4 = Problem(objective=anal_4, features=features_4)

    results_F = []
    results_G_1 = []
    results_G_2 = []
    results_F_3 = []
    results_F_4 = []
    results_G_3 = []
    results_G_4 = []

    samples = [[0, 1], [-3, 2], [0, 0], [-3, -3]]
    samples_3 = [[0], [-3], [2], [0.5]]

    for sample, sample_3 in zip(samples, samples_3):
        results_F.append(anal_1(sample))
        results_F_3.append(anal_3(sample))
        results_F_4.append(anal_4(sample_3))
        results_G_1.append(list(subtract(anal_1(sample), [5, 2000])))
        results_G_2.append([anal_1(sample)[0] - 5])
        results_G_4.append([anal_4(sample_3)[0] - 3])

    def test_evaluate(self):
        F_1, G_1 = TestProblem.problem_1.evaluate(TestProblem.samples)
        self.assertEqual(F_1.all(), array(TestProblem.results_F).all())
        self.assertEqual(G_1.all(), array(TestProblem.results_G_1).all())

        F_3 = TestProblem.problem_3.evaluate(TestProblem.samples)
        self.assertEqual(F_3.all(), array(TestProblem.results_F_3).all())  # type: ignore

        F_4, G_4 = TestProblem.problem_4.evaluate(TestProblem.samples_3)
        self.assertEqual(F_4.all(), array(TestProblem.results_F_4).all())  # type: ignore
        self.assertEqual(G_4.all(), array(TestProblem.results_G_4).all())
