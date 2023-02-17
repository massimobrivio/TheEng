from typing import Tuple

from abstract import Blues
from pandas import DataFrame
from problem import ProblemConstructor
from rankers import Rankers


class Ranker(Blues):
    def __init__(self, problem: ProblemConstructor, data: DataFrame, weights: Tuple):

        if not len(weights) == len(problem.getObjectivesExpressions()):
            raise ValueError("Weights should be the same length as objectives.")

        if not sum(weights) == 1:
            raise ValueError("Weights should sum up to 1.")

        self.problem = problem
        self.data = data
        self.weights = weights

    def do(self, rankingName: str = "topsis"):
        rankingMethod = self._getGreen(
            Rankers,
            rankingName,
            problem=self.problem,
            data=self.data,
            weights=self.weights,
        )
        data = rankingMethod()
        return data
