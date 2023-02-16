from pandas import DataFrame
import plotly.express as px
from plotly.graph_objects import Figure


class Visualizations:
    def __init__(self, data: DataFrame) -> None:
        self.data = data

    def scatterPlot(self, **kwargs) -> Figure:
        xName = kwargs.get("xName")
        yName = kwargs.get("yName")
        visualizationObject = px.scatter(self.data, x=xName, y=yName)
        return visualizationObject

    def heatMap(self, **kwargs) -> Figure:
        columnsNames = kwargs.get("columnsNames")
        filteredData = self.data[columnsNames]  # type: ignore
        visualizationObject = px.imshow(filteredData.corr(), text_auto=".1f")  # type: ignore
        return visualizationObject

    def parallelCoordinate(self, **kwargs) -> Figure:
        columnsNames = kwargs.get("columnsNames")
        filteredData = self.data[columnsNames]  # type: ignore
        visualizationObject = px.parallel_coordinates(
            filteredData, dimensions=list(filteredData.columns)
        )
        return visualizationObject
