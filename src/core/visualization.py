from typing import Union
from abstract import Blues
from visualizations import Visualizations
from pandas import DataFrame


class Visualization(Blues):
    def __init__(self, data: DataFrame):
        self.data = data

    def do(self, visualizationName: str, savePath: Union[None, str] = None, **kwargs):
        visualizationMethod = self._getGreen(
            Visualizations, visualizationName, data=self.data
        )(**kwargs)
        if savePath:
            visualizationMethod.write_html(savePath)
