from abc import ABC, abstractmethod
from difflib import SequenceMatcher
from inspect import getmembers, ismethod
from typing import Callable, Dict, List, Tuple

from problem import ProblemConstructor


class Step(ABC):
    def __init__(
        self,
        problem: ProblemConstructor,
        evaluator: Callable[[Dict[str, float]], Dict[str, float]],
    ):
        self.problem = problem
        self.evaluator = evaluator

        pNames = problem.getPnames()
        objectiveExpressions = problem.getObjectivesExpressions()
        resultsExpressions = problem.getResultsExpressions()

        Step._checkExpressions(pNames, "Parameters Names")
        Step._checkExpressions(objectiveExpressions, "Objectives Names")
        Step._checkExpressions(resultsExpressions, "Results Names")

        self.pNames = pNames
        self.objectives = problem.getObjectives()
        self.constraints = problem.getConstraints()
        self.objectiveExpressions = objectiveExpressions
        self.constraintExpressions = problem.getConstraintsExpressions()
        self.resultsExpressions = resultsExpressions
        self.lowerBounds, self.upperBounds = problem.getBounds()

        self.nVar = len(self.pNames)
        self.nObj = len(self.objectiveExpressions)

    @abstractmethod
    def do(self, **kwargs):
        pass

    def _getMethod(self, classObject: Callable, methodName: str, **kwargs):
        obj = classObject(**kwargs)
        availableMethods = [m[0] for m in getmembers(obj, predicate=ismethod)]
        if methodName not in availableMethods:
            similarMethods, similarity_ratio = Step._findSimilar(
                methodName, availableMethods
            )
            similarMethod = similarMethods[0]
            print(
                f"Method {methodName} not available or misspelled. Using {similarMethod} instead.\nMatching percentage: {round(similarity_ratio[0]*100, 2)} %"
            )
            methodName = similarMethod  # overwrite method with similar method
        samplerMethod = getattr(obj, methodName)
        return samplerMethod

    @staticmethod
    def _findSimilar(
        source_name: str, nameslist: List[str]
    ) -> Tuple[List[str], List[float]]:
        """
        Find similar names to a source name in a list of names.

        Args:
            source_name (str): the name to compare.
            nameslist (List[str]): the list of names to compare with the source name.

        Returns:
            Tuple[List[str], List[float]]: A tuple of sorted lists of similar names and their similarities.
        """
        similar_names_similarity = []
        for name in nameslist:
            similarity = SequenceMatcher(None, source_name, name).ratio()
            if similarity > 0.8:
                similar_names_similarity.append((name, similarity))

        similar_names_similarity.sort(key=lambda x: x[1], reverse=True)
        similar_names = [name for name, _ in similar_names_similarity]
        similarities = [similarity for _, similarity in similar_names_similarity]

        return similar_names, similarities

    @staticmethod
    def _checkExpressions(expressions: List[str], listName: str):
        if not expressions:
            raise ValueError(f"List of {listName} is empty.")
