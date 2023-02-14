from typing import List, Dict

from simulators import Simulators
from abstract import Blues


class Simulator(Blues):
    def __init__(self) -> None:
        self.simulator = None

    def do(self, simulatorName: str, fcdPath: str, resultsRequest: List[str]):
        simulator = self._getGreen(
            Simulators, simulatorName, fcdPath=fcdPath, resultsRequest=resultsRequest
        )
        self.simulator = simulator
        return simulator

    def simulate(self, parameters: Dict[str, float]) -> Dict[str, float]:
        if not self.simulator:
            raise ValueError("No simulator has been generated. Use do() method first.")
        return self.simulator(parameters)


if __name__ == "__main__":
    simulator = Simulator()
    simulator.do(
        "femSimulator",
        "examples\\beam_freecad\\FemCalculixCantilever3D_Param.FCStd",
        ["Disp"],
    )
    results = simulator.simulate({"Length": 2000, "Width": 1000, "Height": 1100})

    print(results)
