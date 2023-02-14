from typing import Tuple, Dict, Callable
from pickle import dump, load
from os.path import isfile

from pandas import DataFrame
from surrogates import Surrogates
from sklearn.model_selection import cross_val_score

from abstract import Blues
from problem import ProblemConstructor
from evaluator import Evaluator


class Surrogate(Blues):
    def __init__(
        self, problem: ProblemConstructor, evaluator: Evaluator, data: DataFrame
    ) -> None:
        super().__init__(problem, evaluator)
        parameterNames = problem.getPnames()
        resultRequest = evaluator.getResultsRequest()
        self.trainingData_x = data[parameterNames].values
        self.trainingData_y = data[resultRequest].values

        self.trainedSurrogate = None
        self.resultRequest = resultRequest

    def do(self, surrogateName: str, save: bool = False, **kwargs):
        surrogateMethod = self._getGreen(Surrogates, surrogateName)(**kwargs)
        trainedSurrogate, surrogatePerformance = self.train(
            surrogateMethod, save=save, **kwargs
        )
        self.trainedSurrogate = trainedSurrogate

        return self.predict, surrogatePerformance

    def doFromFile(self, surrogatePath: str) -> Callable[(...), Dict[str, float]]:
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
        results = dict(zip(self.resultRequest, predictions[0]))
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
    def _checkPath(path: str, *args) -> None:
        if not isfile(path):
            raise FileNotFoundError(args[0])


if __name__ == "__main__":
    from simulator import Simulator
    from sampler import Sampler

    problem = ProblemConstructor()
    problem.setObjectives(["Disp^2"])
    problem.setContraints(["Disp-2"])
    problem.setBounds(
        {"Length": (2000, 5000), "Width": (1000, 3000), "Height": (500, 1500)}
    )

    simul = Simulator()
    simulator = simul.generate(
        "femSimulator",
        "examples\\beam_freecad\\FemCalculixCantilever3D_Param.FCStd",
        ["Disp"],
    )

    evaluator = Evaluator(["Disp"])
    evaluator.setSimulator(simulator)

    sampler = Sampler(problem, evaluator)
    samples, f, data = sampler.do("latinHypercube", 15)

    print(data)

    surrogate = Surrogate(problem, evaluator, data)
    predict, surrogatePerformance = surrogate.do("polynomial", degree_fit=3)

    print(predict({"Length": 1000, "Width": 500, "Height": 1000}))
    print(surrogatePerformance)
