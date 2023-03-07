from typing import Union
from abstract import Step
from algorithms.visualizations import Visualizations
from pandas import DataFrame


class Visualization(Step):
    def __init__(self, data: DataFrame):
        self.data = data

    def do(
        self,
        visualizationName: str = "parallelCoordinate",
        savePath: Union[None, str] = None,
        **kwargs
    ):
        visualizationMethod = self._getMethod(
            Visualizations, visualizationName, data=self.data
        )(**kwargs)
        if savePath:
            visualizationMethod.write_html(savePath)
