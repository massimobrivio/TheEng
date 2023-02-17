from typing import Tuple

from pandas import DataFrame, concat
from problem import ProblemConstructor


class Rankers:
    def __init__(
        self, problem: ProblemConstructor, data: DataFrame, weights: Tuple[float]
    ) -> None:
        self.data = data
        self.objectivesData = data[problem.getObjectivesExpressions()]
        normData = Rankers._normalization(self.objectivesData)
        self.weightedNormData = Rankers._weightening(normData, weights)

    def topsis(self):
        raise NotImplementedError("TOPSIS scoring method not implemented yet.")

    def simpleAdditive(self):
        performanceScore = self.weightedNormData.sum(axis=1)
        resultData = concat(
            [
                self.data,
                DataFrame(
                    performanceScore,
                    columns=[
                        "Score",
                    ],
                ),
            ],
            axis=1,
        )
        sortedResultData = resultData.sort_values("Score", ascending=False)
        sortedResultData = Rankers._returnEfficient(sortedResultData)
        return sortedResultData

    @staticmethod
    def _returnEfficient(data: DataFrame):
        if "Score" in data.columns:
            data["Efficiency"] = [
                True if value < 0.15 else False for value in data["Score"]
            ]
            return data
        return data

    @staticmethod
    def _normalization(data: DataFrame):
        normData = (data - data.min()) / (data.max() - data.min())
        return normData

    @staticmethod
    def _weightening(data: DataFrame, weights: Tuple[float]):
        weightedNormData = data.multiply(weights, axis=1)
        return weightedNormData
