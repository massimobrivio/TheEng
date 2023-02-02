from typing import Callable, List, Union

from theeng.utilities.types import FeatureDefinition
from pandas import DataFrame, concat


class Data:
    """
    Class handling the database for surrogate model training.
    """

    def __init__(
        self, features: FeatureDefinition, simulator: Callable[..., List[float]]
    ) -> None:
        """_summary_

        Args:
            features (FeatureDefinition): _description_
            simulator (Callable[..., List[float]]): _description_
        """
        self.simulator = simulator
        self.pnames = features.pnames
        self.tnames = features.tnames

    def generate(
        self,
        samples: DataFrame,
        fval: Union[DataFrame, None] = None,
    ) -> DataFrame:
        """_summary_

        Args:
            samples (DataFrame): _description_
            fval (Union[DataFrame, ndarray, None], optional): _description_. Defaults to None.

        Returns:
            DataFrame: _description_
        """

        if fval is None:
            fval = self._evaluate(samples)

        data = concat([samples, fval], axis=1)

        return data

    def add(
        self,
        data: DataFrame,
        samples: DataFrame,
        fval: Union[DataFrame, None] = None,
    ) -> DataFrame:
        """_summary_

        Args:
            data (DataFrame): _description_
            samples (DataFrame): _description_
            fval (Union[DataFrame, None], optional): _description_. Defaults to None.

        Returns:
            DataFrame: _description_
        """
        if fval is None:
            fval = self._evaluate(samples)

        new_data = concat([samples, fval], axis=1)
        data = concat([data, new_data], axis=0)

        return data

    def _evaluate(self, samples: DataFrame) -> DataFrame:
        """_summary_

        Args:
            samples (DataFrame): _description_

        Returns:
            DataFrame: _description_
        """
        fval = []

        for _, x in samples.iterrows():
            fval.append(self.simulator(x.to_list()))

        fval = DataFrame(fval, columns=self.tnames)

        return fval
