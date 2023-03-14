from os.path import isfile
from typing import Callable, Dict

from theeng.algorithms.simulators import Simulators
from theeng.core.abstract import Step
from theeng.core.problem import ProblemConstructor


class Simulator(Step):
    def __init__(self, problem: ProblemConstructor) -> None:
        self.resultsExpressions = problem.getResultsExpressions()
        self.iterableOutput = problem.getIterableOutput()
        self.simulator = None

    def generate(
        self, simulatorName: str, fcdPath: str
    ) -> Callable[[Dict[str, float]], Dict[str, float]]:
        if not isfile(fcdPath):
            raise FileNotFoundError(
                f"FreeCAD file at {fcdPath} was not found. Check path or filename."
            )
        simulator = self._getMethod(
            Simulators,
            simulatorName,
            resultsExpressions=self.resultsExpressions,
            iterableOutput=self.iterableOutput,
            fcdPath=fcdPath,
        )
        self.simulator = simulator
        return simulator

    def simulate(self, parameters: Dict[str, float]) -> Dict[str, float]:
        if not self.simulator:
            raise ValueError("No simulator has been generated. Use do() method first.")
        return self.simulator(parameters)
