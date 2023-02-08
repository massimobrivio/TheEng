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
        """Initialize Latin Hypercube sampling.

        Args:
            problem_constructor (ProblemConstructor): The optimization problem.
            evaluator (Evaluator): The evaluator.
        """
        super().__init__(problem_constructor, evaluator)

    def _algorithm(
        self,
        n_samples: int,
        lower_bounds: List[float],
        upper_bounds: List[float],
        nvar: int,
    ) -> List[List[float]]:
        """_summary_

        Args:
            n_samples (int): number of samples to generate.
            lower_bounds (List[float]): lower bounds of the design space.
            upper_bounds (List[float]): upper bounds of the design space.
            nvar (int): number of variables in the design space.

        Returns:
            List[List[float]]: A list of samples to be evaluated
        """
        sampler = qmc.LatinHypercube(d=nvar)
        samp = sampler.random(n=n_samples)
        samples = qmc.scale(samp, lower_bounds, upper_bounds).tolist()

        return samples


if __name__ == "__main__":
    from evaluator import FEModelEvaluator

    problem = ProblemConstructor()
    problem.set_objectives(["Disp^2"])
    problem.set_contraints(["Disp-2"])
    problem.set_bounds(
        {"Length": (2000, 5000), "Width": (1000, 3000), "Height": (500, 1500)}
    )

    evaluator = FEModelEvaluator(
        problem, ["Disp"], "examples\\beam_freecad\\FemCalculixCantilever3D_Param.FCStd"
    )

    sampler = LatinHypercube(problem, evaluator)
    x, f, data = sampler.sample(4)

    print(f"Data: {data}")
    print("------------------")

    surrogate, surrogate_performance = evaluator.generate_surrogate(
        data, method="polynomal"
    )

    parameters = {"Length": 3050.0, "Width": 2200.0, "Height": 1001}

    print(f"Surrogate performance: {surrogate_performance}")
    print(f"Surrogate prediction: {evaluator.evaluate(parameters, use_surrogate=True)}")
