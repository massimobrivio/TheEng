from typing import Callable, Dict, List, Iterable, Union
from os.path import isfile
from pickle import load

from simulator import Simulator


class Evaluator:
    """class for evaluators."""

    def __init__(
        self,
        resultsRequest: List[str],
        path_to_fcd_file: str,
        path_to_surrogate: Union[str, None] = None,
    ) -> None:
        """Initialize evaluator.

        Args:
            problem_constructor (ProblemConstructor): The problem to be evaluated.
            results_request (List[str]): A list of results aliases contained in the spreadsheet which are to be returned.
            path_to_fcd_file (str): The path to the FreeCAD file containing the model.
            path_to_surrogate (Union[str, None], optional): The path to the surrogate file. Defaults to None.

        """

        Evaluator._checkList(
            resultsRequest,
            str,
            "results_request must be iterable.",
            "results_request must contain strings.",
        )
        Evaluator._checkPath(
            path_to_fcd_file, 
            f"No path to FreeCAD file found at {path_to_fcd_file}."
            )

        self.surrogate = None
        self.simulator = None

        self.path_to_fcd_file = path_to_fcd_file
        self.path_to_surrogate = path_to_surrogate

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
            return self._evaluateSurrogate(parameters)
        else:
            return self._evaluateSimulator(parameters)

    def setSurrogate(self, surrogate):
        pass  # to implement

    def setSimulator(self, simulatorName: str):
        self.simulator = Simulator()
        self.simulator.setSimulator(simulatorName)

    def _evaluateSurrogate(self, parameters: Dict[str, float]) -> Dict[str, float]:
        """Method to evaluate the surrogate model.

        Args:
            parameters (Dict[str, float]): A dicttionary of design parameters values and their aliases contained in the spreadsheet (names).

        Raises:
            ValueError: If no surrogate has been generated.

        Returns:
            Dict[str, float]: A dictionary containing results aliases and values.
        """
        if not self.surrogate:  # Surrogate not loaded
            try:  # Try to load surrogate from file
                Evaluator._checkPath(
                    self.path_to_surrogate,
                    "No path to surrogate file specified. Please specify a path to load the surrogate.",
                )
                print(f"Trying to load surrogate from file... {self.path_to_surrogate}")
                self.surrogate = load(open(self.path_to_surrogate, "rb"))
            except FileNotFoundError:
                raise ValueError(
                    "No surrogate has been generated. Run method generate_surrogate first."
                )
        predictions = self.surrogate.predict([list(parameters.values())])
        results = dict(zip(self.results_request, predictions[0]))
        return results

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
