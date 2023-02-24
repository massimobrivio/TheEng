from typing import Callable, Dict

from abstract import Blues
from problem import ProblemConstructor
from simulators import Simulators


class Simulator(Blues):
    def __init__(self, problem: ProblemConstructor) -> None:
        self.resultsExpressions = problem.getResultsExpressions()
        self.iterableOutput = problem.getIterableOutput()
        self.simulator = None

    def do(
        self, simulatorName: str, fcdPath: str
    ) -> Callable[[Dict[str, float]], Dict[str, float]]:
        simulator = self._getGreen(
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


if __name__ == "__main__":
    problem = ProblemConstructor()
    problem.setObjectives(["Disp^2"])
    problem.setContraints(["Disp-2"])
    problem.setBounds(
        {"Length": (2000, 5000), "Width": (1000, 3000), "Height": (500, 1500)}
    )
    problem.setResults({"Disp": None})

    simulator = Simulator(problem)
    simulator.do(
        "femSimulator", "examples\\beam_freecad_multiobj\\FemCalculixCantilever3D_Param.FCStd"
    )
    results = simulator.simulate({"Length": 2000, "Width": 1000, "Height": 1100})

    print("Displacement it: ", results["Disp"], " mm")
