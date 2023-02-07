from typing import List

from abstract import Evaluator, Sampler
from problem import ProblemConstructor
from scipy.stats import qmc


class LatinHypercube(Sampler):
    """
    Class for Latin design space sampling.
    """

    def __init__(
        self, problem_constructor: ProblemConstructor, evaluator: Evaluator
    ) -> None:
        super().__init__(problem_constructor, evaluator)

    def _algorithm(
        self,
        n_samples: int,
        lower_bounds: List[float],
        upper_bounds: List[float],
        nvar: int,
    ) -> List[List[float]]:
        """Implementation of Latin Hypercube sampling.

        Args:
            n_samples (int, optional): Number of samples to generate.

        Returns:
            ndarray: Numpy array of samples.
        """
        sampler = qmc.LatinHypercube(d=nvar)
        samp = sampler.random(n=n_samples)
        samples = qmc.scale(samp, lower_bounds, upper_bounds).tolist()

        return samples


if __name__ == "__main__":
    from evaluator import FEModelEvaluator

    obj_expression = ["Disp^2"]
    const_expression = ["Disp-2"]

    problem = ProblemConstructor()
    problem.set_objectives(obj_expression)
    problem.set_contraints(const_expression)
    problem.set_bounds({"Length": (2000, 5000), "Width": (1000, 3000), "Height": (500, 1500)})

    evaluator = FEModelEvaluator(
        ["Disp"], "examples\\beam_freecad\\FemCalculixCantilever3D_Param.FCStd"
    )

    sampler = LatinHypercube(problem, evaluator)
    x, f, r = sampler.sample(3)

    print(f"Design variables: {x}")
    print(f"Objectives: {f}")
    print(f"Total: {r}")
    print("------------------\n")

