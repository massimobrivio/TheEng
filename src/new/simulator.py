from typing import Tuple, List, Dict, Callable
from inspect import getmembers, ismethod
from difflib import SequenceMatcher

from simulators import Simulators


class Simulator:
    def __init__(self) -> None:
        self.simulator = None

    def generate(
        self, simulatorName: str, fcdPath: str, resultsRequest: List[str]
    ) -> Callable:
        simulator = Simulator._getSimulator(simulatorName, fcdPath, resultsRequest)
        self.simulator = simulator  # could add to a list of simulator so that we can create multiple simulators from different files.
        return simulator  # type: ignore

    def simulate(self, parameters: Dict[str, float]) -> Dict[str, float]:
        if not self.simulator:
            raise ValueError(
                "No simulator has been generated. Use generate() method first."
            )
        return self.simulator(parameters)

    @staticmethod
    def _getSimulator(
        simulatorName: str, fcdPath: str, resultsRequest: List[str]
    ) -> None:
        simulators = Simulators(resultsRequest, fcdPath)
        availableSimulators = [m[0] for m in getmembers(simulators, predicate=ismethod)]
        if simulatorName not in availableSimulators:
            similarMethods, similarity_ratio = Simulator._findSimilar(
                simulatorName, availableSimulators
            )
            similarMethod = similarMethods[0]
            print(
                f"Method {simulatorName} not available or misspelled. Using {similarMethod} instead.\n Matching percentage: {round(similarity_ratio[0]*100, 2)} %"
            )
            simulatorName = similarMethod  # overwrite method with similar method
        simulator = getattr(simulators, simulatorName)
        return simulator

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


if __name__ == "__main__":
    simulator = Simulator()
    simulator.generate(
        "femSimulator",
        "examples\\beam_freecad\\FemCalculixCantilever3D_Param.FCStd",
        ["Disp"],
    )
    results = simulator.simulate({"Length": 2000, "Width": 1000, "Height": 1100})

    print(results)
