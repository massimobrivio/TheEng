from abc import ABC, abstractmethod
from collections import defaultdict
from typing import Dict, List, Tuple, Union

from numpy import concatenate
from problem import ProblemConstructor
from pymoo.core.callback import Callback
from pymoo.core.population import Population
from pymoo.core.problem import ElementwiseProblem
from pymoo.operators.sampling.rnd import FloatRandomSampling
from pymoo.optimize import minimize


class Evaluator(ABC):
    """Abstract class for simulation evaluators."""

    def __init__(
        self,
        results_request: List[str],
        path_to_fcd_file: str,
    ) -> None:
        """_summary_

        Args:
            results_request (List[str]): list of results aliases contained in the spreadsheet.
            path_to_fcd_file (str): path to the FreeCAD file containing the model.
        """
        self.path_to_fcd_file = path_to_fcd_file
        self.results_request = results_request

    @abstractmethod
    def evaluate(self, parameters: Dict[str, float]) -> Dict[str, float]:
        """Evaluate the design parameters and return the results by updating the spreadsheet and running the FEM analysis in FreeCAD.

        Args:
            parameters (Dict[str, float]): dictionary of design parameters containing aliases and values contained in the spreadsheet.
        """
        pass


class Sampler(ABC):
    """Abstract class for sampling strategies."""

    def __init__(
        self, problem_constructor: ProblemConstructor, evaluator: Evaluator
    ) -> None:
        """Initialize the sampler.

        Args:
            problem_constructor (ProblemConstructor): _description_
            evaluator (Evaluator): _description_
        """
        self.problem_constructor = problem_constructor
        self.evaluator = evaluator

    def sample(self, n_samples: int = 50) -> Tuple:
        """Sample the design space.

        Args:
            n_samples (int, optional): _description_. Defaults to 50.

        Returns:
            Tuple: _description_
        """

        problem = SamplingProblem(self.problem_constructor, self.evaluator)
        x = self._algorithm(
            n_samples, problem._lower_bounds, problem._upper_bounds, problem._nvar
        )

        out = defaultdict(list)
        res = problem._evaluate(x, out)  # type: ignore

        f = res["F"]
        r = res["R"]

        return x, f, r

    @abstractmethod
    def _algorithm(
        self,
        n_samples: int,
        lower_bounds: List[float],
        upper_bounds: List[float],
        nvar: int,
    ) -> List[List[float]]:
        """Implement the sampling algorithm.

        Args:
            n_samples (int): _description_
            lower_bounds (List[float]): _description_
            upper_bounds (List[float]): _description_
            nvar (int): _description_

        Returns:
            List[List[float]]: _description_
        """
        pass


class SamplingProblem:
    def __init__(self, problem_constructor: ProblemConstructor, evaluator: Evaluator):
        """Initialize the sampling problem.

        Args:
            problem_constructor (ProblemConstructor): _description_
            evaluator (Evaluator): _description_
        """
        self._evaluator = evaluator

        self._nvar = problem_constructor.get_nvar()
        self._pnames = problem_constructor.get_pnames()

        self._objectives = problem_constructor.get_objectives()
        self._constraints = problem_constructor.get_constraints()
        self._lower_bounds, self._upper_bounds = problem_constructor.get_bounds()

    def _evaluate(
        self, x: List[List[float]], out: Dict[str, List[List[float]]], *args, **kwargs
    ) -> Dict[str, List[List[float]]]:
        """Evaluate the sampling problem on the given samples.

        Args:
            x (List[List[float]]): _description_
            out (Dict[str, List[List[float]]]): _description_

        Returns:
            Dict[str, List[List[float]]]: _description_
        """
        f = []
        g = []
        r = []

        for sample in x:
            parameters = {name: value for name, value in zip(self._pnames, sample)}
            results = self._evaluator.evaluate(parameters)

            objs = [obj(results) for obj in self._objectives]
            consts = [constr(results) for constr in self._constraints]
            res = list(results.values()) + objs + consts

            f.append(objs)
            g.append(consts)
            r.append(res)

        out["F"] = f
        out["G"] = g
        out["R"] = r

        return out


class Optimizer(ABC):
    def __init__(
        self,
        problem_constructor: ProblemConstructor,
        evaluator: Evaluator,
        restart_pop: Union[FloatRandomSampling, Population] = FloatRandomSampling(),
    ) -> None:
        """Initialize the optimizer.

        Args:
            problem_constructor (ProblemConstructor): _description_
            evaluator (Evaluator): _description_
            restart_pop (Union[FloatRandomSampling, Population], optional): _description_. Defaults to FloatRandomSampling().
        """
        self.problem_constructor = problem_constructor
        self.evaluator = evaluator
        self.restart_pop = restart_pop

    def optimize(self, termination: Tuple[str, int]) -> Tuple:
        """Optimize the design.

        Args:
            termination (Tuple[str, int]): _description_

        Returns:
            Tuple: _description_
        """

        problem = OptimizationProblem(self.problem_constructor, self.evaluator)
        algorithm = self._algorithm()

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

        return x, f, x_hist, r_hist

    @abstractmethod
    def _algorithm(self):
        pass


class OptimizationProblem(ElementwiseProblem):
    def __init__(self, problem_constructor: ProblemConstructor, evaluator: Evaluator):
        """Initialize the optimization problem.

        Args:
            problem_constructor (ProblemConstructor): _description_
            evaluator (Evaluator): _description_
        """

        self._evaluator = evaluator

        self._nvar = problem_constructor.get_nvar()
        self._nobj = problem_constructor.get_nobj()
        self._nconst = problem_constructor.get_nconst()
        self._pnames = problem_constructor.get_pnames()

        self._objectives = problem_constructor.get_objectives()
        self._constraints = problem_constructor.get_constraints()
        self._lower_bounds, self._upper_bounds = problem_constructor.get_bounds()

        super().__init__(
            n_var=self._nvar,
            n_obj=self._nobj,
            n_constr=self._nconst,
            xl=self._lower_bounds,
            xu=self._upper_bounds,
        )

    def _evaluate(self, x, out, *args, **kwargs):

        parameters = {
            name: value for name, value in zip(self._pnames, x)
        }  # probably does not work
        results = self._evaluator.evaluate(parameters)  # type: ignore

        f = [obj(results) for obj in self._objectives]
        g = [constr(results) for constr in self._constraints]
        r = list(results.values())

        out["F"] = f
        out["G"] = g
        out["R"] = r + f + g


class HistCallback(Callback):
    def __init__(self) -> None:
        super().__init__()
        self.data["x_hist"] = []
        self.data["r_hist"] = []

    def notify(self, algorithm):
        self.data["x_hist"].append(algorithm.pop.get("X"))
        self.data["r_hist"].append(algorithm.pop.get("R"))
