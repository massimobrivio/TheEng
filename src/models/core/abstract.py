from abc import ABC, abstractmethod
from typing import Dict, List
from problem import ProblemConstructor
from numpy import ndarray


class Evaluator(ABC):
    """Abstract class for simulation evaluators."""

    def __init__(
        self,
        results_request: List[str],
        path_to_fcd_file: str,
    ) -> None:
        """_summary_

        Args:
            results_request (List[str]): list of results aliases contained in the spreadsheet.
            path_to_fcd_file (str): path to the FreeCAD file containing the model.
        """
        self.path_to_fcd_file = path_to_fcd_file
        self.results_request = results_request

    @abstractmethod
    def evaluate(self, parameters: Dict[str, float]) -> Dict[str, float]:
        """Evaluate the design parameters and return the results by updating the spreadsheet and running the FEM analysis in FreeCAD.

        Args:
            parameters (Dict[str, float]): dictionary of design parameters containing aliases and values contained in the spreadsheet.
        """
        pass


class Sampler(ABC):
    """Abstract class for sampling strategies."""

    def __init__(self, problem: ProblemConstructor) -> None:
        """Initialize the sampler.

        Args:
            problem (ProblemConstructor): The problem constructor object.
        """
        self.lower_bounds, self.upper_bounds = problem.get_bounds()
        self.nvar = problem.nvar
        self.pnames = problem.pnames

    def sample(self, evaluator: Evaluator) -> List[List[float]]:
        """Evaluate the samples using the evaluator.

        Args:
            evaluator (Evaluator): The evaluator object.

        Returns:
            List[List[float]]: The database of design samples and results.
        """
        database = []
        samples = self._method()
        for sample in samples:
            parameters = dict.fromkeys(self.pnames, sample)
            results = evaluator.evaluate(parameters)
            data = sample.tolist() + list(results.values())
            database.append(data)
        return database

    @abstractmethod
    def _method(self, n_samples: int = 50) -> ndarray:
        """Implement the sampling method."""
        pass
