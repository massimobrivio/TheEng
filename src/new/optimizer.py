from difflib import SequenceMatcher
from inspect import getmembers, ismethod
from typing import List, Tuple

from evaluator import Evaluator
from numpy import concatenate
from optimizers import Optimizers
from pandas import DataFrame
from problem import ProblemConstructor
from pymoo.core.callback import Callback
from pymoo.core.problem import ElementwiseProblem
from pymoo.optimize import minimize


class Optimizer:
    def __init__(self, problem: ProblemConstructor, evaluator: Evaluator) -> None:
        self.problem = problem
        self.evaluator = evaluator

        self.pname = problem.getPnames()
        self.objectiveExpressions = problem.getObjectivesExpressions()
        self.constraintExpressions = problem.getConstraintsExpressions()
        self.lowerBounds, self.upperBounds = problem.getBounds()
        self.resultsExpressions = evaluator.getResultsRequest()

        self.nVar = len(self.pname)

        self.optimizer = None

    def optimize(
        self,
        optimizerName: str,
        termination: Tuple[str, int],
        useSurrogate: bool = False,
        **kwargs
    ):

        problem = OptimizationProblem(
            self.problem, self.evaluator, useSurrogate=useSurrogate
        )
        algorithm = self._getOptimizer(optimizerName)(**kwargs)

        res = minimize(
            problem,
            algorithm,
            termination=termination,
            seed=1,
            callback=HistCallback(),
            return_least_infeasible=True,
        )

        x = res.X.tolist()
        f = res.F.tolist()
        x_hist = concatenate(res.algorithm.callback.data["x_hist"]).tolist()
        r_hist = concatenate(res.algorithm.callback.data["r_hist"]).tolist()

        data = concatenate([x_hist, r_hist], axis=1)
        data = DataFrame(
            data,
            columns=self.pname
            + self.resultsExpressions
            + self.objectiveExpressions
            + self.constraintExpressions,
        )

        data = data.T.drop_duplicates().T  # drop duplicate columns

        return x, f, data

    def _getOptimizer(self, optimizerName: str):
        optimizers = Optimizers()
        availableOptimizers = [m[0] for m in getmembers(optimizers, predicate=ismethod)]
        if optimizerName not in availableOptimizers:
            similarMethods, similarity_ratio = Optimizer._findSimilar(
                optimizerName, availableOptimizers
            )
            similarMethod = similarMethods[0]
            print(
                f"Method {optimizerName} not available or misspelled. Using {similarMethod} instead.\n Matching percentage: {round(similarity_ratio[0]*100, 2)} %"
            )
            optimizerName = similarMethod  # overwrite method with similar method
        optimizerMethod = getattr(optimizers, optimizerName)
        return optimizerMethod

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


class OptimizationProblem(ElementwiseProblem):
    def __init__(
        self,
        problem: ProblemConstructor,
        evaluator: Evaluator,
        useSurrogate: bool = False,
    ):
        """Initialize the optimization problem.

        Args:
            problem (ProblemConstructor): The problem to be evaluated.
            evaluator (Evaluator): The evaluator to be used.
        """

        self._useSurrogate = useSurrogate
        self._evaluator = evaluator

        self._nvar = problem.getNvar()
        self._nobj = problem.getNobj()
        self._nconst = problem.getNconst()
        self._pnames = problem.getPnames()

        self._objectives = problem.getObjectives()
        self._constraints = problem.getConstraints()
        self._lowerBounds, self._upperBounds = problem.getBounds()

        super().__init__(
            n_var=self._nvar,
            n_obj=self._nobj,
            n_constr=self._nconst,
            xl=self._lowerBounds,
            xu=self._upperBounds,
        )

    def _evaluate(self, x, out: dict, *args, **kwargs):
        """Evaluate the optimization problem on the given designs.

        Args:
            x (_type_): Design samples.
            out (dict): dictionary containing the evaluated samples, objectives and constraints.
        """

        parameters = {name: value for name, value in zip(self._pnames, x)}
        results = self._evaluator.evaluate(parameters, useSurrogate=self._useSurrogate)

        f = [obj(results) for obj in self._objectives]
        g = [constr(results) for constr in self._constraints]
        r = list(results.values())

        out["F"] = f
        out["G"] = g
        out["R"] = r + f + g


class HistCallback(Callback):
    """A class to store the all history of the optimization process."""

    def __init__(self) -> None:
        super().__init__()
        self.data["x_hist"] = []
        self.data["r_hist"] = []

    def notify(self, algorithm):
        self.data["x_hist"].append(algorithm.pop.get("X"))
        self.data["r_hist"].append(algorithm.pop.get("R"))


if __name__ == "__main__":
    from simulator import Simulator


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

    optimizer = Optimizer(problem, evaluator)
    x, f, data = optimizer.optimize("geneticAlgorithm", ("n_eval", 6), popSize=3)

    print(data)