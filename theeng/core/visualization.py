from typing import Union

from pandas import DataFrame

from theeng.algorithms.visualizations import Visualizations
from theeng.core.abstract import Step


class Visualization(Step):
    def __init__(self, data: DataFrame):
        self.data = data

    def plot(
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
