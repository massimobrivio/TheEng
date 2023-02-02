from typing import Callable, List, Union
from theeng.utilities.types import Optimization
from pymoo.algorithms.moo.unsga3 import NSGA3
from pymoo.algorithms.soo.nonconvex.ga import GA
from pymoo.algorithms.soo.nonconvex.nelder import NelderMead
from pymoo.algorithms.soo.nonconvex.pso import PSO
from pymoo.factory import get_reference_directions
from pymoo.operators.sampling.rnd import FloatRandomSampling
from pymoo.core.population import Population


class NelderMeadSearch(Optimization):
    def __init__(
        self, objective: Callable[..., List[float]], features, popsize
    ) -> None:
        """

        :param features: Collective targets and parameters information in the form of FeatureDefinition class
        :type features: FeatureDefinition
        :param popsize: population size to use in evolutionary algorithms (global optimization)
        :type popsize: int
        """
        super().__init__(objective, features, popsize)

    def _algorithm(self):
        return NelderMead()


class GeneticAlgorithm(Optimization):
    def __init__(
        self, objective: Callable[..., List[float]], features, popsize,
        restart_pop: Union[FloatRandomSampling, Population] = FloatRandomSampling()
    ) -> None:
        """

        :param features: Collective targets and parameters information in the form of FeatureDefinition class
        :type features: FeatureDefinition
        :param popsize: population size to use in evolutionary algorithms (global optimization)
        :type popsize: int
        """
        super().__init__(objective, features, popsize, restart_pop)

    def _algorithm(self):
        return GA(pop_size=self.popsize, eliminate_duplicates=True, sampling=self.restart_pop)  # type: ignore


class ParticleSwarm(Optimization):
    def __init__(
        self, objective: Callable[..., List[float]], features, popsize,
        restart_pop: Union[FloatRandomSampling, Population] = FloatRandomSampling()
    ) -> None:
        """

        :param features: Collective targets and parameters information in the form of FeatureDefinition class
        :type features: FeatureDefinition
        :param popsize: population size to use in evolutionary algorithms (global optimization)
        :type popsize: int
        """
        super().__init__(objective, features, popsize, restart_pop)

    def _algorithm(self):
        return PSO(pop_size=self.popsize, sampling=self.restart_pop)  # type: ignore


class NSGA_III(Optimization):
    def __init__(
        self, objective: Callable[..., List[float]], features, popsize,
        restart_pop: Union[FloatRandomSampling, Population] = FloatRandomSampling()
    ) -> None:
        """

        :param features: Collective targets and parameters information in the form of FeatureDefinition class
        :type features: FeatureDefinition
        :param popsize: population size to use in evolutionary algorithms (global optimization)
        :type popsize: int
        """
        super().__init__(objective, features, popsize, restart_pop)

    def _algorithm(self):
        """
        Method defining the optimization algorithm.
        For multi-objective problems NSGA-III is used.

        :return: The algorithm object.
        :rtype:

        See https://pymoo.org/algorithms/moo/nsga3.html for more information.
        """
        ref_dirs = get_reference_directions(
            "energy", self.features.nobjs, n_points=10, seed=1
        )
        algorithm = NSGA3(
            pop_size=self.popsize, ref_dirs=ref_dirs, eliminate_duplicates=True, sampling=self.restart_pop  # type: ignore
        )

        return algorithm
