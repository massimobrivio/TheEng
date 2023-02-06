from abstract import Sampler
from scipy.stats import qmc
from problem import ProblemConstructor
from numpy import ndarray


class LatinHypercube(Sampler):
    """
    Class for Latin design space sampling.
    """

    def __init__(self, problem: ProblemConstructor) -> None:
        super().__init__(problem)

    def _method(self, n_samples: int = 50) -> ndarray:
        """Implementation of Latin Hypercube sampling.

        Args:
            n_samples (int, optional): Number of samples to generate. Defaults to 50.

        Returns:
            ndarray: Numpy array of samples.
        """
        sampler = qmc.LatinHypercube(d=self.nvar)
        samp = sampler.random(n=n_samples)
        samples = qmc.scale(samp, self.lower_bounds, self.upper_bounds)

        return samples

