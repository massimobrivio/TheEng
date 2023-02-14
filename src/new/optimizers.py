from typing import Union

from pymoo.algorithms.moo.unsga3 import NSGA3
from pymoo.algorithms.soo.nonconvex.ga import GA
from pymoo.algorithms.soo.nonconvex.nelder import NelderMead
from pymoo.algorithms.soo.nonconvex.pso import PSO
from pymoo.core.population import Population
from pymoo.factory import get_reference_directions
from pymoo.operators.sampling.rnd import FloatRandomSampling


class Optimizers:
    def __init__(self) -> None:
        pass

    def nelderMead(self):
        return NelderMead()

    def geneticAlgorithm(
        self,
        popSize: int,
        restartPop: Union[FloatRandomSampling, Population] = FloatRandomSampling(),
    ):
        return GA(pop_size=popSize, eliminate_duplicates=True, sampling=restartPop)  # type: ignore

    def particleSwarm(
        self,
        popSize: int,
        restartPop: Union[FloatRandomSampling, Population] = FloatRandomSampling(),
    ):
        return PSO(pop_size=popSize, sampling=restartPop)  # type: ignore

    def nsga3(
        self,
        popSize: int,
        nObj: int,
        restartPop: Union[FloatRandomSampling, Population] = FloatRandomSampling(),
    ):
        ref_dirs = get_reference_directions("energy", nObj, n_points=nObj + 1, seed=1)
        return NSGA3(pop_size=popSize, ref_dirs=ref_dirs, eliminate_duplicates=True, sampling=restartPop)  # type: ignore
