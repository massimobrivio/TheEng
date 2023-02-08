from typing import Union

from abstract import Evaluator, Optimizer
from problem import ProblemConstructor
from pymoo.algorithms.moo.unsga3 import NSGA3
from pymoo.algorithms.soo.nonconvex.ga import GA
from pymoo.algorithms.soo.nonconvex.nelder import NelderMead
from pymoo.algorithms.soo.nonconvex.pso import PSO
from pymoo.core.population import Population
from pymoo.factory import get_reference_directions
from pymoo.operators.sampling.rnd import FloatRandomSampling


class NelderMeadSearch(Optimizer):
    def __init__(
        self, problem_constructor: ProblemConstructor, evaluator: Evaluator
    ) -> None:
        super().__init__(problem_constructor, evaluator)

    def _algorithm(self):
        return NelderMead()


class GeneticAlgorithm(Optimizer):
    def __init__(
        self,
        problem_constructor: ProblemConstructor,
        evaluator: Evaluator,
        popsize: int,
        restart_pop: Union[FloatRandomSampling, Population] = FloatRandomSampling(),
    ) -> None:
        self.popsize = popsize
        super().__init__(problem_constructor, evaluator, restart_pop)

    def _algorithm(self):
        return GA(pop_size=self.popsize, eliminate_duplicates=True, sampling=self.restart_pop)  # type: ignore


class ParticleSwarm(Optimizer):
    def __init__(
        self,
        problem_constructor: ProblemConstructor,
        evaluator: Evaluator,
        popsize: int,
        restart_pop: Union[FloatRandomSampling, Population] = FloatRandomSampling(),
    ) -> None:
        self.popsize = popsize
        super().__init__(problem_constructor, evaluator, restart_pop)

    def _algorithm(self):
        return PSO(pop_size=self.popsize, sampling=self.restart_pop)  # type: ignore


class NSGA_III(Optimizer):
    def __init__(
        self,
        problem_constructor: ProblemConstructor,
        evaluator: Evaluator,
        popsize: int,
        restart_pop: Union[FloatRandomSampling, Population] = FloatRandomSampling(),
    ) -> None:
        self.popsize = popsize
        super().__init__(problem_constructor, evaluator, restart_pop)

    def _algorithm(self):
        nobj = self.problem_constructor.get_nobj()
        ref_dirs = get_reference_directions("energy", nobj, n_points=nobj + 1, seed=1)
        algorithm = NSGA3(
            pop_size=self.popsize, ref_dirs=ref_dirs, eliminate_duplicates=True, sampling=self.restart_pop  # type: ignore
        )

        return algorithm


if __name__ == "__main__":
    from evaluator import FEModelEvaluator

    obj_expression = ["Disp"]
    const_expression = ["Disp-2"]

    problem = ProblemConstructor()
    problem.set_objectives(obj_expression)
    problem.set_contraints(const_expression)
    problem.set_bounds(
        {"Length": (2000, 5000), "Width": (1000, 3000), "Height": (500, 1500)}
    )

    evaluator = FEModelEvaluator(
        problem, ["Disp"], "examples\\beam_freecad\\FemCalculixCantilever3D_Param.FCStd"
    )

    optimizer = GeneticAlgorithm(problem, evaluator, 3)
    x, f, data = optimizer.optimize(("n_eval", 6))
    print(f"Data:\n {data}")
