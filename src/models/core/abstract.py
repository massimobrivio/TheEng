from abc import ABC, abstractmethod
from typing import Dict, List


class Evaluator(ABC):
    """Abstract class for simulation evaluators."""

    def __init__(
        self,
        parameters: Dict[str, float],
        results_request: List[str],
        path_to_fcd_file: str,
    ) -> None:
        """_summary_

        Args:
            parameters (Dict[str, float]): dictionary of design parameters containing aliases and values contained in the spreadsheet.
            results_request (List[str]): list of results aliases contained in the spreadsheet.
            path_to_fcd_file (str): path to the FreeCAD file containing the model.
        """
        self.path_to_fcd_file = path_to_fcd_file
        self.parameters = parameters
        self.results_request = results_request

    @abstractmethod
    def evaluate(self) -> Dict[str, float]:
        """Evaluate the design parameters and return the results by updating the spreadsheet and running the FEM analysis in FreeCAD."""
        pass
