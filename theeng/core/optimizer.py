from typing import Callable, Dict, Iterable, List, Tuple

from numpy import concatenate
from pandas import DataFrame
from pymoo.core.callback import Callback
from pymoo.core.problem import ElementwiseProblem
from pymoo.optimize import minimize

from theeng.algorithms.optimizers import Optimizers
from theeng.core.abstract import Step
from theeng.core.problem import ProblemConstructor

from multiprocessing.pool import ThreadPool
from pymoo.core.problem import StarmapParallelization

n_threads = 4
pool = ThreadPool(n_threads)
runner = StarmapParallelization(pool.starmap)


class Optimizer(Step):
    def __init__(
        self,
        problem: ProblemConstructor,
        evaluator: Callable[[Dict[str, float]], Dict[str, float]],
    ) -> None:
        super().__init__(problem, evaluator)

    def optimize(
        self,
        optimizerName: str = "nsga3",
        termination: Tuple[str, int] = ("n_eval", 100),
        **kwargs
    ) -> Tuple[List[List[float]], List[List[float]], DataFrame]:
        if self.nObj > 1:
            if not optimizerName == "nsga3":
                raise Exception(
                    "Only NSGA3 is supported for multi-objective optimization. Use nsga3 name."
                )

        problem = OptimizationProblem(self.problem, self.evaluator, elementwise_runner=runner)
        algorithm = self._getMethod(Optimizers, optimizerName)(**kwargs, nObj=self.nObj)

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

        if not isinstance(x[0], Iterable):
            x = [x]
        if not isinstance(f[0], Iterable):
            f = [f]

        x_hist = concatenate(res.algorithm.callback.data["x_hist"]).tolist()
        r_hist = concatenate(res.algorithm.callback.data["r_hist"]).tolist()

        data = concatenate([x_hist, r_hist], axis=1)
        data = DataFrame(
            data,
            columns=self.pNames
            + self.resultsExpressions
            + self.objectiveExpressions
            + self.constraintExpressions,
        )

        data = data.T.drop_duplicates().T  # drop duplicate columns

        return x, f, data

    def convertToSimulator(
        self,
        x: List[List[float]],
        simulator: Callable[[Dict[str, float]], Dict[str, float]],
    ) -> Tuple[List[List[float]], List[List[float]], DataFrame]:
        f = []
        r = []

        for design in x:
            parameters = {name: value for name, value in zip(self.pNames, design)}
            results = simulator(parameters)

            objs = [obj(results) for obj in self.objectives]
            consts = [constr(results) for constr in self.constraints]
            res = list(results.values()) + objs + consts

            f.append(objs)
            r.append(res)

        data = concatenate([x, r], axis=1)
        data = DataFrame(
            data,
            columns=self.pNames
            + self.resultsExpressions
            + self.objectiveExpressions
            + self.constraintExpressions,
        )

        data = data.T.drop_duplicates().T

        return x, f, data


class OptimizationProblem(ElementwiseProblem):
    def __init__(
        self,
        problem: ProblemConstructor,
        evaluator: Callable[[Dict[str, float]], Dict[str, float]],
        **kwargs
    ):
        """Initialize the optimization problem.

        Args:
            problem (ProblemConstructor): The problem to be evaluated.
            evaluator (Evaluator): The evaluator to be used.
        """

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
        results = self._evaluator(parameters)

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
