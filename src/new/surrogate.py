from typing import Tuple, List, Dict
from inspect import getmembers, ismethod
from difflib import SequenceMatcher
from pickle import dump

from pandas import DataFrame
from surrogates import Surrogates
from sklearn.model_selection import cross_val_score


class Surrogate:
    def __init__(self) -> None:
        self.surrogate = None
        self.surrogate_performance = None

    def predict(self, parameters: Dict[str, float]) -> Dict[str, float]:
        """Method to evaluate the surrogate model.

        Args:
            parameters (Dict[str, float]): A dicttionary of design parameters values and their aliases contained in the spreadsheet (names).

        Raises:
            ValueError: If no surrogate has been generated.

        Returns:
            Dict[str, float]: A dictionary containing results aliases and values.
        """
        predictions = self.surrogate.predict([list(parameters.values())])
        results = dict(zip(self.results_request, predictions[0]))
        return results

    def train(
        self,
        data: DataFrame,
        method: str,
        parameterNames: List[str],
        resultRequest: List[str],
        save: bool = False,
        **kwargs,
    ) -> None:
        training_data_x = data[parameterNames].values
        training_data_y = data[resultRequest].values

        self.setSurrogate(method, **kwargs)
        self.surrogate = self.surrogate.fit(training_data_x, training_data_y)

        n_data_rows = len(data)
        test_set_numdata = (
            n_data_rows * 0.2
        )  # 20% of the data is used for testing in cross validation.
        n_kfold_splits = (
            round(n_data_rows / test_set_numdata) if test_set_numdata > 2 else 2
        )
        scores = cross_val_score(
            self.surrogate, training_data_x, training_data_y, cv=n_kfold_splits
        )
        self.surrogate_performance = (scores.mean(), scores.std())

        if save:
            if not self.path_to_surrogate:
                raise ValueError(
                    "No path to surrogate file specified. Please specify a path to save the surrogate."
                )
            with open(self.path_to_surrogate, "wb") as f:
                dump(self.surrogate, f)
            f.close()

        return self.surrogate, self.surrogate_performance

    def setSurrogate(self, surrogateName: str) -> None:
        surrogates = Surrogates()
        availableSurrogates = [m[0] for m in getmembers(surrogates, predicate=ismethod)]
        if surrogateName not in availableSurrogates:
            similarMethods, similarity_ratio = Surrogate._findSimilar(
                method, availableSurrogates
            )
            similarMethod = similarMethods[0]
            print(
                f"Method {method} not available or misspelled. Using {similarMethod} instead.\n Matching percentage: {round(similarity_ratio[0]*100, 2)} %"
            )
            method = similarMethod  # overwrite method with similar method
        self.surrogate = getattr(surrogates, surrogateName)

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
