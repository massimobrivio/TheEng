from abstract import Blues
from problem import ProblemConstructor
from pandas import DataFrame
from typing import Tuple
from rankers import Rankers


class Ranker(Blues):
    def __init__(self, problem: ProblemConstructor, data: DataFrame, weights: Tuple[float]):
        self.problem = problem
        self.data = data
        self.weights = weights

    def do(self, rankingName: str):
        rankingMethod = self._getGreen(Rankers, rankingName, problem=self.problem, data=self.data, weights=self.weights)
        data = rankingMethod()
        return data