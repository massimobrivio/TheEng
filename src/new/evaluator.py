from typing import Callable, Dict, List, Iterable, Union
from os.path import isfile


class Evaluator:
    """class for evaluators."""

    def __init__(self, resultsRequest: List[str]) -> None:
        """Initialize evaluator.

        Args:
            resultsRequest (List[str]): A list of results aliases contained in the spreadsheet which are to be returned.
            fcdPath (str): The path to the FreeCAD file containing the model.
            surrogatePath (Union[str, None], optional): The path to the surrogate file. Defaults to None.

        """

        Evaluator._checkList(
            resultsRequest,
            str,
            "results_request must be iterable.",
            "results_request must contain strings.",
        )

        self.surrogate = None
        self.simulator = None
        self.resultsRequest = resultsRequest

    def evaluate(
        self, parameters: Dict[str, float], useSurrogate=False
    ) -> Dict[str, float]:
        """A method to evaluate the design parameters and return the results. Both the simulator and the surrogate can be used.

        Args:
            parameters (Dict[str, float]): A dicttionary of design parameters values and their aliases contained in the spreadsheet (names).
            useSurrogate (bool, optional): Wether to use a surrogate instead of the simulator. Defaults to False.

        Returns:
            Dict[str, float]: A dictionary containing results aliases and values.
        """
        if useSurrogate:
            return self.surrogate(parameters)  # type: ignore
        else:
            return self.simulator(parameters)  # type: ignore

    def setSurrogate(self, surrogate: Callable[(...), Dict[str, float]]):
        self.surrogate = surrogate

    def setSimulator(self, simulator: Callable[(...), Dict[str, float]]):
        self.simulator = simulator

    def getResultsRequest(self) -> List[str]:
        return self.resultsRequest

    @staticmethod
    def _checkPath(path: str, *args) -> None:
        if not isfile(path):
            raise FileNotFoundError(args[0])

    @staticmethod
    def _checkList(list: List[str], type: Callable, *args) -> None:
        if not isinstance(list, Iterable):
            raise TypeError(args[0])
        if not all([isinstance(result, type) for result in list]):
            raise TypeError(args[1])
