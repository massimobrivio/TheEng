from os.path import isfile
from pickle import dump, load
from typing import Callable, Dict, Tuple

from abstract import Blues
from pandas import DataFrame
from problem import ProblemConstructor
from sklearn.model_selection import cross_val_score
from surrogates import Surrogates


class Surrogate(Blues):
    def __init__(
        self,
        problem: ProblemConstructor,
        data: DataFrame,
    ) -> None:
        parameterNames = problem.getPnames()
        resultsExpressions = problem.getResultsExpressions()
        self.trainingData_x = data[parameterNames].values
        self.trainingData_y = data[resultsExpressions].values

        self.trainedSurrogate = None
        self.resultsExpressions = resultsExpressions

    def do(
        self, surrogateName: str = "polynomial", save: bool = False, **kwargs
    ) -> Tuple[Callable[[Dict[str, float]], Dict[str, float]], Tuple[float, float]]:
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
        results = dict(zip(self.resultsExpressions, predictions[0]))
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
    from os.path import join

    from optimizer import Optimizer
    from pandas import concat
    from ranker import Ranker
    from sampler import Sampler
    from simulator import Simulator
    from visualization import Visualization

    wd = "C:\\Users\\mgbri\\Desktop\\"

    problem = ProblemConstructor()
    problem.setResults({"Disp": "Max", "Stress": "Max", "Length": None})
    problem.setObjectives(["-Disp", "Stress"])
    problem.setContraints(["3000 - Length"])
    problem.setBounds(
        {"Length": (2000, 5000), "Width": (1000, 3000), "Height": (500, 1500)}
    )

    simul = Simulator(problem)
    simulator = simul.do(
        "femSimulator",
        "examples\\beam_freecad_multiobj\\FemCalculixCantilever3D_Param.FCStd",
    )

    sampler = Sampler(problem, simulator)
    xSamp, fSamp, dataSamp = sampler.do("latinHypercube", 10)

    surrog = Surrogate(problem, dataSamp)
    surrogate, surrogatePerformance = surrog.do(
        "polynomial", save=True, degree_fit=3, surrogatePath=join(wd, "surrogate.pkl")
    )

    optimizer = Optimizer(problem, surrogate)
    xOpt, fOpt, dataOptSur = optimizer.do("nsga3", ("n_eval", 200), popSize=10)
    xOpt, fOpt, dataOpt = optimizer.convertToSimulator(xOpt, simulator)

    print("Optimizer data are: \n", dataOpt)

    ranker = Ranker(
        problem,
        concat([dataSamp, dataOpt]),
        weights=(0.6, 0.4),
        constraintsRelaxation=[
            30,
        ],
    )
    dataRanked = ranker.do("simpleAdditive")

    print("Ranked results are: \n", dataRanked)

    visualizer = Visualization(dataRanked)
    visualizer.do("scatterPlot", join(wd, "scatter.html"), xName="Disp", yName="Stress")
    visualizer.do("parallelCoordinate", join(wd, "parallel_coord.html"))
    visualizer.do("heatMap", join(wd, "heatmap.html"))
