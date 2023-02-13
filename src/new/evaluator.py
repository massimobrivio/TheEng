from typing import Callable, Dict, List, Iterable, Union
from os.path import isfile
from pickle import load

from simulator import Simulator


class Evaluator:
    """class for evaluators."""

    def __init__(
        self,
        resultsRequest: List[str],
        fcdPath: str,
        surrogatePath: Union[str, None] = None,
    ) -> None:
        """Initialize evaluator.

        Args:
            problem_constructor (ProblemConstructor): The problem to be evaluated.
            results_request (List[str]): A list of results aliases contained in the spreadsheet which are to be returned.
            fcdPath (str): The path to the FreeCAD file containing the model.
            surrogatePath (Union[str, None], optional): The path to the surrogate file. Defaults to None.

        """

        Evaluator._checkList(
            resultsRequest,
            str,
            "results_request must be iterable.",
            "results_request must contain strings.",
        )
        Evaluator._checkPath(
            fcdPath, 
            f"No path to FreeCAD file found at {fcdPath}."
            )

        self.surrogate = None
        self.simulator = None

        self.path_to_fcd_file = fcdPath
        self.path_to_surrogate = surrogatePath

    def evaluate(
        self, parameters: Dict[str, float], use_surrogate=False
    ) -> Dict[str, float]:
        """A method to evaluate the design parameters and return the results. Both the simulator and the surrogate can be used.

        Args:
            parameters (Dict[str, float]): A dicttionary of design parameters values and their aliases contained in the spreadsheet (names).
            use_surrogate (bool, optional): Wether to use a surrogate instead of the simulator. Defaults to False.

        Returns:
            Dict[str, float]: A dictionary containing results aliases and values.
        """
        if use_surrogate:
            return self.surrogate(parameters)
        else:
            return self.simulator(parameters)

    def setSurrogate(self, surrogate: Callable[(...), Dict[str, float]]):
        self.surrogate = surrogate

    def setSimulator(self, simulator: Callable[(...), Dict[str, float]]):
        self.simulator = simulator

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
