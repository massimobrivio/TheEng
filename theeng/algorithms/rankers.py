from math import sqrt
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
        bestDesign = self.weightedNormData.min(axis=0)
        worstDesign = self.weightedNormData.max(axis=0)
        performanceScore = []
        for _, design in self.weightedNormData.iterrows():
            positiveSeparation = sqrt(sum((design - bestDesign) ** 2))
            negativeSeparation = sqrt(sum((design - worstDesign) ** 2))
            performanceScore.append(
                negativeSeparation / (negativeSeparation + positiveSeparation)
            )
        resultData = concat(
            [
                self.data.reset_index(drop=True),
                DataFrame(
                    performanceScore,
                    columns=[
                        "Score",
                    ],
                ),
            ],
            axis=1,
        )
        sortedResultData = resultData.sort_values("Score", ascending=True)  # sure is ascending?
        sortedResultData = Rankers._returnEfficient(sortedResultData)
        return sortedResultData

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
        sortedResultData = resultData.sort_values("Score", ascending=True)
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
