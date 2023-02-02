import unittest
from theeng.blocks.sampling import Latin
from theeng.utilities.types import FeatureDefinition, Parameter, Target


class TestSampling(unittest.TestCase):

    x1 = Parameter("x1", 0, 2)
    f1 = Target("f1", 0.5, True, 5)
    f2 = Target("f2", 0.5, False, 5)
    f3 = Target("f3", 0.5, False, None)
    features = FeatureDefinition([x1], [f1, f2])
    lat = Latin(features)

    def test_state(self):
        self.assertEqual(len(TestSampling.lat.lbs), TestSampling.lat.nvar)
        self.assertEqual(len(TestSampling.lat.ubs), TestSampling.lat.nvar)

    def test_call(self):
        samples = TestSampling.lat(n_samples=10)
        self.assertEqual(samples.shape[0], 10)
        self.assertEqual(samples.shape[1], 1)
