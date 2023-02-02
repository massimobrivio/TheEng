from typing import Callable, List, Dict
from theeng.utilities.types import FeatureDefinition


class AnalyticalInterface:
    def __init__(
        self, simulator: Callable[(...), Dict[str, float]], features: FeatureDefinition
    ) -> None:
        self.simulator = simulator
        self.tnames = features.tnames

    def objective(self, x: list) -> List[float]:
        temp = self.simulator(x)
        results = [temp[tname] for tname in self.tnames]
        return results
