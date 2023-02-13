from typing import Tuple, List, Dict, Callable
from inspect import getmembers, ismethod
from difflib import SequenceMatcher
from pickle import dump, load
from os.path import isfile

from pandas import DataFrame
from surrogates import Surrogates
from sklearn.model_selection import cross_val_score


class Surrogate:
    def __init__(
        self, data: DataFrame, parameterNames: List[str], resultRequest: List[str]
    ) -> None:
        self.trainingData_x = data[parameterNames].values
        self.trainingData_y = data[resultRequest].values

        self.trainedSurrogate = None
        self.results_request = resultRequest

    def generate(
        self, surrogateName: str, save: bool = False, **kwargs
    ):
        surrogateMethod = Surrogate._getSurrogate(surrogateName)
        trainedSurrogate, surrogatePerformance = self.train(
            surrogateMethod, save=save, **kwargs
        )
        self.trainedSurrogate = trainedSurrogate

        return self.predict, surrogatePerformance

    def getFromFile(self, surrogatePath: str) -> Callable[(...), Dict[str, float]]:
        try:  # Try to load surrogate from file
            Surrogate._checkPath(
                surrogatePath,
                "No path to surrogate file specified. Please specify a path to load the surrogate.",
            )
            print(f"Trying to load surrogate from file... {surrogatePath}")
            trainedSurrogate = load(open(surrogatePath, "rb"))
            self.trainedSurrogate = trainedSurrogate
        except FileNotFoundError:
            raise ValueError(
                "No surrogate has been generated. Run method generate_surrogate first."
            )
        return self.predict

    def predict(self, parameters: Dict[str, float]) -> Dict[str, float]:
        """Method to evaluate the surrogate model.

        Args:
            parameters (Dict[str, float]): A dicttionary of design parameters values and their aliases contained in the spreadsheet (names).

        Raises:
            ValueError: If no surrogate has been generated.

        Returns:
            Dict[str, float]: A dictionary containing results aliases and values.
        """
        if not self.trainedSurrogate:
            raise ValueError(
                "No surrogate has been generated. Use train() method first."
            )
        predictions = self.trainedSurrogate.predict([list(parameters.values())])  # type: ignore        
        results = dict(zip(self.results_request, predictions[0]))
        return results

    def train(
        self,
        surrogateMethod,
        save: bool = False,
        **kwargs,
    ) -> Tuple[object, Tuple[float, float]]:
        trainedSurrogate = surrogateMethod.fit(self.trainingData_x, self.trainingData_y)

        n_data_rows = len(self.trainingData_x)
        test_set_numdata = (
            n_data_rows * 0.2
        )  # 20% of the data is used for testing in cross validation.
        n_kfold_splits = (
            round(n_data_rows / test_set_numdata) if test_set_numdata > 2 else 2
        )
        scores = cross_val_score(
            trainedSurrogate,
            self.trainingData_x,
            self.trainingData_y,
            cv=n_kfold_splits,
        )
        surrogatePerformance = (scores.mean(), scores.std())

        if save:
            if not kwargs.get("surrogatePath"):
                raise ValueError(
                    "No path specified. Please specify a path to save the surrogate."
                )
            with open(kwargs.get("surrogatePath"), "wb") as f:  # type: ignore
                dump(trainedSurrogate, f)
            f.close()

        return trainedSurrogate, surrogatePerformance

    @staticmethod
    def _getSurrogate(surrogateName: str) -> Callable:
        surrogates = Surrogates()
        availableSurrogates = [m[0] for m in getmembers(surrogates, predicate=ismethod)]
        if surrogateName not in availableSurrogates:
            similarMethods, similarity_ratio = Surrogate._findSimilar(
                surrogateName, availableSurrogates
            )
            similarMethod = similarMethods[0]
            print(
                f"Method {surrogateName} not available or misspelled. Using {similarMethod} instead.\n Matching percentage: {round(similarity_ratio[0]*100, 2)} %"
            )
            surrogateName = similarMethod  # overwrite method with similar method
        surrogateMethod = getattr(surrogates, surrogateName)
        return surrogateMethod

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

    @staticmethod
    def _checkPath(path: str, *args) -> None:
        if not isfile(path):
            raise FileNotFoundError(args[0])
