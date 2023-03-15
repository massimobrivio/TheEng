import numpy as np
from pandas import DataFrame

from theeng.algorithms.rankers import Rankers
from theeng.core.abstract import Step
from theeng.core.problem import ProblemConstructor


class Ranker(Step):
    def __init__(self, problem: ProblemConstructor, data: DataFrame) -> None:
        objectiveExpressions = problem.getObjectivesExpressions()
        constraintsExpressions = problem.getConstraintsExpressions()
        objectiveWeights = problem.getObjectiveWeights()
        constraintsRelaxation = problem.getConstraintsRelaxation()

        if not len(objectiveWeights) == len(objectiveExpressions):
            raise ValueError("Weights should be the same length as objectives.")

        if not sum(objectiveWeights) == 1:
            raise ValueError("Weights should sum up to 1.")

        if not len(constraintsRelaxation) == len(constraintsExpressions):
            raise ValueError(
                "Constraints relaxation should be the same length as constraints expressions."
            )

        elif constraintsRelaxation is None:
            constraintsRelaxation = [np.inf] * len(constraintsExpressions)

        for i in range(len(constraintsRelaxation)):
            minConstraintViolation = np.min(data[constraintsExpressions[i]])
            if constraintsRelaxation[i] < minConstraintViolation:
                print(
                    "Warning: Relaxation value is smaller than the minimum value of the constraint expression."
                )
                print(
                    f"Relaxation value will be set to the minimum value of the constraint expression -> {minConstraintViolation}"
                )
                constraintsRelaxation[i] = minConstraintViolation

        # get constraints expressions for which relaxation is not None
        constraintsRelaxationExpressions = [
            constraintsExpressions[i]
            for i in range(len(constraintsExpressions))
            if constraintsRelaxation[i] is not None
        ]
        # filter data with different conditions for each constraint column
        data = data[data[constraintsRelaxationExpressions].apply(lambda x: all(x <= constraintsRelaxation[i] for i, x in enumerate(x)), axis=1)]  # type: ignore

        self.problem = problem
        self.data = data
        self.objectiveWeights = objectiveWeights

    def rank(self, rankingName: str = "topsis"):
        rankingMethod = self._getMethod(
            Rankers,
            rankingName,
            problem=self.problem,
            data=self.data,
            weights=self.objectiveWeights,
        )
        data = rankingMethod()
        return data
