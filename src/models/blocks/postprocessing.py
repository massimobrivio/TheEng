from typing import List, Union
from warnings import warn

import mcdm
import plotly.express as px
from src.utilities.types import Visualization
from numpy import abs, where, array, multiply
from numpy.linalg import norm as npnorm
from src.utilities.types import FeatureDefinition
from pandas import DataFrame
from plotly.graph_objects import Figure


class Decision:
    """
    Class implementing Multi-Criteria Decision-Making (MCDM) techniques.
    """

    def __init__(
        self,
        features: FeatureDefinition,
        rank_type: str = "TOPSIS",
        weight_type: str = "MW",
        norm_type: str = "Vector",
    ) -> None:
        """_summary_

        Args:
            data (DataFrame): _description_
            features (FeatureDefinition): _description_
            rank_type (str, optional): _description_. Defaults to "TOPSIS".
            weight_type (str, optional): _description_. Defaults to "MW".
            norm_type (str, optional): _description_. Defaults to "Vector".
        """

        onames = []
        weights = []

        for tname, is_objective, is_min, weight in zip(
            features.tnames,
            features.are_objective.values(),
            features.are_minimizations.values(),
            features.weights.values(),
        ):
            if is_objective:
                onames.append(tname)
                if is_min:
                    weights.append(weight)
                else:
                    weights.append(-weight)

        weights = array(weights)
        if sum(abs(weights)) != 1:
            norm = npnorm(abs(weights))
            if norm == 0:
                raise ZeroDivisionError(
                    "Weights where provided not normalized. Could not attempt auto-normalization (norm is 0). Please, normalize the weights."
                )
            else:
                weights = weights / norm
            warn(f"Weights where provided not normalized. Normalizing to {weights}.")

        self.onames = onames
        self.weights = weights
        self.abs_weights = abs(weights)
        self.rank_type = rank_type
        self.weight_type = weight_type
        self.norm_type = norm_type

    def decide(self, data: DataFrame, return_choices: int = 10) -> DataFrame:
        """_summary_

        Args:
            data (DataFrame): _description_
            return_choices (int, optional): _description_. Defaults to 10.

        Returns:
            DataFrame: _description_
        """
        alternatives = data[self.onames].values
        ranked_sol = mcdm.rank(
            alternatives,
            w_vector=self.abs_weights,
            alt_names=list(range(len(alternatives))),
            is_benefit_x=[False if weight >= 0 else True for weight in self.weights],
            n_method=self.norm_type,
            w_method=self.weight_type,
            s_method=self.rank_type,
        )
        bests_id = [sol[0] for sol in ranked_sol]
        is_eff = [
            True if i in bests_id[:return_choices] else False
            for i in range(data.shape[0])
        ]
        data["efficiency"] = where(is_eff, "Efficient", "Sub-Optimal")

        return data


class ScatterPlot(Visualization):
    """
    Implementation of Scatter plot visualization of the Pareto-Front.
    """

    def __init__(
        self,
        data: DataFrame,
        pareto_x: str,
        pareto_y: str,
        save: bool = True,
        figname: str = "pareto.html",
        **kwargs,
    ) -> None:
        """_summary_

        Args:
            data (DataFrame): _description_
            pareto_x (str): _description_
            pareto_y (str): _description_
            save (bool, optional): _description_. Defaults to True.
            figname (str, optional): _description_. Defaults to "pareto.html".
        """
        self.pareto_x = pareto_x
        self.pareto_y = pareto_y
        super().__init__(data, save, figname, **kwargs)

    def _method(self, data, **kwargs) -> Figure:
        """_summary_

        Args:
            data (_type_): _description_

        Returns:
            Figure: _description_
        """
        if "efficiency" in data:
            m = px.scatter(data, x=self.pareto_x, y=self.pareto_y, color="efficiency")
        else:
            m = px.scatter(data, x=self.pareto_x, y=self.pareto_y)
        return m


class HeatMap(Visualization):
    """
    Implementation of Heatmap plot to visualize parameter correlations.
    """

    def __init__(
        self,
        data: DataFrame,
        columns: Union[List[str], None] = None,
        save: bool = True,
        figname: str = "correlations.html",
        **kwargs,
    ) -> None:
        """_summary_

        Args:
            data (DataFrame): _description_
            columns (Union[List[str], None], optional): _description_. Defaults to None.
            save (bool, optional): _description_. Defaults to True.
            figname (str, optional): _description_. Defaults to "correlations.html".
        """
        self.columns = columns
        super().__init__(data, save, figname, **kwargs)

    def _method(self, data, **kwargs) -> Figure:
        """_summary_

        Args:
            data (_type_): _description_

        Returns:
            Figure: _description_
        """
        if self.columns and set(self.columns).issubset(data.columns):
            data = data[self.columns]
        m = px.imshow(data.corr(), text_auto=".1f")  # type: ignore
        return m


class ParallelCoord(Visualization):
    def __init__(
        self,
        data: DataFrame,
        columns: Union[List[str], None] = None,
        save: bool = True,
        figname: str = "parallelcoord.html",
        **kwargs,
    ):
        self.columns = columns
        super().__init__(data, save, figname, **kwargs)

    def _method(self, data, **kwargs) -> Figure:
        """_summary_

        Args:
            data (_type_): _description_

        Returns:
            Figure: _description_
        """
        if self.columns and set(self.columns).issubset(data.columns):
            data = data[self.columns]
        m = px.parallel_coordinates(data, dimensions=list(data.columns))
        return m


class Convergence(Visualization):
    def __init__(
        self,
        data: DataFrame,
        features: FeatureDefinition,
        save: bool = True,
        figname: str = "convergence.html",
        **kwargs,
    ):

        self.weights = []
        self.onames = []

        for tname, is_objective, weight in zip(
            features.tnames, features.are_objective.values(), features.weights.values()
        ):
            if is_objective:
                self.onames.append(tname)
                self.weights.append(weight)

        super().__init__(data, save, figname, **kwargs)

    def _method(self, data: DataFrame, **kwargs) -> Figure:
        data_add = data.copy()
        data_add["objective value"] = data[self.onames].agg(
            lambda x, w: sum(multiply(w, x)), axis=1, w=self.weights
        )
        m = px.line(
            data_add,
            x=list(data.index),
            y="objective value",
            markers=True,
            title="Objective value with iterations",
        )
        return m
