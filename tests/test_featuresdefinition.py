import unittest
from theeng.utilities.types import Parameter, Target, FeatureDefinition


class TestFeatureDefinition(unittest.TestCase):
    p1 = Parameter("p1", 0, 1)
    p2 = Parameter("p2", -0.1, 0.5)
    f1 = Target("f1", 0.5, ineq=1, is_objective=True, is_constraint=True)
    f2 = Target("f2", 0.5, ineq=-5, is_objective=False, is_constraint=True)
    f3 = Target("f3", 0.5, ineq=-5, is_objective=False, is_constraint=True)
    features = FeatureDefinition([p1, p2], [f1, f2])

    def test_init(self):
        self.assertEqual(TestFeatureDefinition.features.pnames, ["p1", "p2"])
        self.assertEqual(TestFeatureDefinition.features.lbs, {"p1": 0.0, "p2": -0.1})
        self.assertEqual(TestFeatureDefinition.features.ubs, {"p1": 1.0, "p2": 0.5})
        self.assertEqual(TestFeatureDefinition.features.nvar, 2)

        self.assertEqual(TestFeatureDefinition.features.tnames, ["f1", "f2"])
        self.assertEqual(TestFeatureDefinition.features.weights, {"f1": 0.5, "f2": 0.5})
        self.assertEqual(
            TestFeatureDefinition.features.are_objective, {"f1": True, "f2": False}
        )
        self.assertEqual(TestFeatureDefinition.features.ineqs, {"f1": 1.0, "f2": -5.0})

        self.assertEqual(len(TestFeatureDefinition.features.weights), 2)
        self.assertEqual(len(TestFeatureDefinition.features.are_objective), 2)
        self.assertEqual(len(TestFeatureDefinition.features.ineqs), 2)

    def test_errors(self):
        with self.assertRaises(Exception) as context:
            features_error1 = FeatureDefinition(
                [TestFeatureDefinition.p1, TestFeatureDefinition.p2], []
            )
            features_error2 = FeatureDefinition(
                [], [TestFeatureDefinition.f1, TestFeatureDefinition.f2]
            )
            features_error3 = FeatureDefinition(
                [TestFeatureDefinition.p1, TestFeatureDefinition.p2],
                [TestFeatureDefinition.f2, TestFeatureDefinition.f3],
            )
