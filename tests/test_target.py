import unittest
from theeng.utilities.types import Target


class TestParameter(unittest.TestCase):

    f1 = Target(
        "f1",
        0.5,
        ineq=1,
        is_objective=True,
        is_minimization=False,
        is_constraint=True,
        is_measurement=False,
    )

    def test_state(self):
        self.assertEqual(TestParameter.f1.name, "f1")
        self.assertEqual(TestParameter.f1.weight, 0.5)
        self.assertEqual(TestParameter.f1.is_objective, True)
        self.assertEqual(TestParameter.f1.is_minimization, False)
        self.assertEqual(TestParameter.f1.ineq, 1)

        self.assertIsInstance(TestParameter.f1.weight, float)
        self.assertIsInstance(TestParameter.f1.is_objective, bool)
        self.assertEqual(
            (isinstance(TestParameter.f1.ineq, float) or TestParameter.f1.ineq is None),
            True,
        )

    def test_repr(self):
        self.assertEqual(
            TestParameter.f1.__repr__(),
            "Target('f1', 0.5, 1.0, True, False, True, False)",
        )
