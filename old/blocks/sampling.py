from src.utilities.types import Sampling, FeatureDefinition
from numpy.random import uniform
from scipy.stats import qmc
from pandas import DataFrame


class Random(Sampling):
    """
    Class for random design space sampling.
    """

    def __init__(self, features: FeatureDefinition) -> None:
        """_summary_

        Args:
            features (FeatureDefinition): _description_
        """
        super().__init__(features)

    def _method(self, n_samples: int = 50) -> DataFrame:
        """_summary_

        Args:
            n_samples (int, optional): _description_. Defaults to 50.

        Returns:
            DataFrame: _description_
        """
        temp = uniform(self.lbs, self.ubs, (n_samples, self.nvar))
        samples = DataFrame(temp, columns=self.features.pnames)

        return samples


class Latin(Sampling):
    """
    Class for Latin design space sampling.
    """

    def __init__(self, features: FeatureDefinition) -> None:
        """_summary_

        Args:
            features (FeatureDefinition): _description_
        """
        super().__init__(features)

    def _method(self, n_samples: int = 50) -> DataFrame:
        """_summary_

        Args:
            n_samples (int, optional): _description_. Defaults to 50.

        Returns:
            DataFrame: _description_
        """
        sampler = qmc.LatinHypercube(d=self.nvar)
        samp = sampler.random(n=n_samples)
        temp = qmc.scale(samp, self.lbs, self.ubs)
        samples = DataFrame(temp, columns=self.features.pnames)

        return samples
