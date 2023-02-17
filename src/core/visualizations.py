from pandas import DataFrame
import plotly.express as px
from plotly.graph_objects import Figure


class Visualizations:
    def __init__(self, data: DataFrame) -> None:
        self.data = data

    def scatterPlot(self, **kwargs) -> Figure:
        xName = kwargs.get("xName")
        yName = kwargs.get("yName")
        if xName in self.data.columns and yName in self.data.columns:
            if "Efficiency" in self.data.columns:
                visualizationObject = px.scatter(self.data, x=xName, y=yName, color="Efficiency")
            else:
                visualizationObject = px.scatter(self.data, x=xName, y=yName)
        else:
            raise ValueError("xName or yName are not present in data.")
        return visualizationObject

    def heatMap(self, **kwargs) -> Figure:
        filteredData = self._filterData(**kwargs)
        visualizationObject = px.imshow(filteredData.corr(), text_auto=".1f")  # type: ignore
        return visualizationObject

    def parallelCoordinate(self, **kwargs) -> Figure:
        filteredData = self._filterData(**kwargs)
        visualizationObject = px.parallel_coordinates(
            filteredData, dimensions=list(filteredData.columns)
        )
        return visualizationObject

    def _filterData(self, **kwargs):
        columnsNames = kwargs.get("columnsNames")
        if columnsNames:
            filteredData = self.data[columnsNames]
        else:
            print("Using all data for visualization...")
            filteredData = self.data
        return filteredData
