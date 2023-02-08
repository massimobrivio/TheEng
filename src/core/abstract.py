from abc import ABC, abstractmethod
from collections import defaultdict
from inspect import getmembers, ismethod
from json import load as json_load
from os.path import isfile, join
from pickle import dump, load
from typing import Dict, Iterable, List, Tuple, Union

from numpy import concatenate
from pandas import DataFrame
from problem import ProblemConstructor
from pymoo.core.callback import Callback
from pymoo.core.population import Population
from pymoo.core.problem import ElementwiseProblem
from pymoo.operators.sampling.rnd import FloatRandomSampling
from pymoo.optimize import minimize
from sklearn.model_selection import cross_val_score
from sklearn.pipeline import Pipeline
from surrogate import Surrogate
from utilities import find_similar


class Evaluator(ABC):
    """Abstract class for simulation evaluators."""

    def __init__(
        self,
        problem_constructor: ProblemConstructor,
        results_request: List[str],
        path_to_fcd_file: str,
        path_to_surrogate: Union[str, None] = None,
    ) -> None:
        """Initialize evaluator.

        Args:
            problem_constructor (ProblemConstructor): The problem to be evaluated.
            results_request (List[str]): A list of results aliases contained in the spreadsheet which are to be returned.
            path_to_fcd_file (str): The path to the FreeCAD file containing the model.
            path_to_surrogate (Union[str, None], optional): The path to the surrogate file. Defaults to None.

        """
        self.problem_constructor = problem_constructor

        if not isinstance(results_request, Iterable):
            raise TypeError("Results request must be Iterable.")
        if not all([isinstance(result, str) for result in results_request]):
            raise TypeError("All results request must be encoded as strings.")

        self.results_request = results_request

        if not isfile(path_to_fcd_file):
            raise FileNotFoundError(
                "The FreeCAD file was not found. Check name and path."
            )

        self.path_to_fcd_file = path_to_fcd_file
        self.path_to_surrogate = path_to_surrogate

        self.surrogate = None
        self.surrogate_performance = None

    def evaluate(
        self, parameters: Dict[str, float], use_surrogate=False
    ) -> Dict[str, float]:
        """A method to evaluate the design parameters and return the results. Both the simulator and the surrogate can be used.

        Args:
            parameters (Dict[str, float]): A dicttionary of design parameters values and their aliases contained in the spreadsheet (names).
            use_surrogate (bool, optional): Wether to use a surrogate instead of the simulator. Defaults to False.

        Returns:
            Dict[str, float]: A dictionary containing results aliases and values.
        """
        if use_surrogate:
            return self._evaluateSurrogate(parameters)
        else:
            return self._evaluateSimulator(parameters)

    def generate_surrogate(
        self, data: DataFrame, method: str = "polynomial", save: bool = False, **kwargs
    ) -> Tuple[Pipeline, Tuple[float, float]]:
        """A method to generate a surrogate model.

        Args:
            data (DataFrame): The dataframe containing the training data.
            method (str, optional): The surrogare method to use. Defaults to "polynomial".
            save (bool, optional): Wether to save the surrogate model to a file. Defaults to False.

        Returns:
            Tuple[Pipeline, Tuple[float, float]]: A tuple containing the surrogate model and its performance.
        """

        training_data_x = data[self.problem_constructor.get_pnames()].values
        training_data_y = data[self.results_request].values

        surrogate = Surrogate()

        available_surrogates = [m[0] for m in getmembers(surrogate, predicate=ismethod)]
        if method not in available_surrogates:
            similar_methods, similarity_ratio = find_similar(
                method, available_surrogates
            )
            similar_method = similar_methods[0]
            print(
                f"Method {method} not available or misspelled. Using {similar_method} instead.\n Matching percentage: {round(similarity_ratio[0]*100, 2)} %"
            )
            method = similar_method  # overwrite method with similar method

        pipe = getattr(surrogate, method)(
            **kwargs
        )  # get relevant method from Surrogate class
        self.surrogate = pipe.fit(training_data_x, training_data_y)

        n_data_rows = len(data)
        test_set_numdata = n_data_rows * 0.2  # 20% of the data is used for testing in cross validation.
        n_kfold_splits = round(n_data_rows/test_set_numdata) if test_set_numdata > 2 else 2
        scores = cross_val_score(self.surrogate, training_data_x, training_data_y, cv=n_kfold_splits)
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

    def _evaluateSurrogate(self, parameters: Dict[str, float]) -> Dict[str, float]:
        """Method to evaluate the surrogate model.

        Args:
            parameters (Dict[str, float]): A dicttionary of design parameters values and their aliases contained in the spreadsheet (names).

        Raises:
            ValueError: If no surrogate has been generated.

        Returns:
            Dict[str, float]: A dictionary containing results aliases and values.
        """
        if not self.surrogate:  # Surrogate not loaded
            try:  # Try to load surrogate from file
                if not self.path_to_surrogate:
                    raise ValueError(
                        "No path to surrogate file specified. Please specify a path to load the surrogate."
                    )
                print(f"Trying to load surrogate from file... {self.path_to_surrogate}")
                self.surrogate = load(open(self.path_to_surrogate, "rb"))
            except FileNotFoundError:
                raise ValueError(
                    "No surrogate has been generated. Run method generate_surrogate first."
                )
        predictions = self.surrogate.predict([list(parameters.values())])
        results = dict(zip(self.results_request, predictions[0]))
        return results

    @abstractmethod
    def _evaluateSimulator(self, parameters: Dict[str, float]) -> Dict[str, float]:
        pass

    def get_results_request(self) -> List[str]:
        return self.results_request


class Sampler(ABC):
    """Abstract class for sampling strategies."""

    def __init__(
        self, problem_constructor: ProblemConstructor, evaluator: Evaluator
    ) -> None:
        """Initialize the sampler.

        Args:
            problem_constructor (ProblemConstructor): The problem to be evaluated.
            evaluator (Evaluator): The evaluator to be used.
        """
        self.problem_constructor = problem_constructor
        self.pname = problem_constructor.get_pnames()
        self.evaluator = evaluator
        self.objective_expressions = problem_constructor.get_objectives_expressions()
        self.constraint_expressions = problem_constructor.get_constraints_expressions()
        self.results_expressions = evaluator.get_results_request()

    def sample(self, n_samples: int = 50) -> Tuple:
        """Sample the design space.

        Args:
            n_samples (int, optional): number of samples to generate. Defaults to 50.

        Returns:
            Tuple: The samples, the objective values and the results.
        """

        problem = SamplingProblem(self.problem_constructor, self.evaluator)
        x = self._algorithm(
            n_samples, problem._lower_bounds, problem._upper_bounds, problem._nvar
        )

        out = defaultdict(list)
        res = problem._evaluate(x, out)  # type: ignore

        f = res["F"]
        r = res["R"]

        data = concatenate([x, r], axis=1)
        data = DataFrame(
            data,
            columns=self.pname
            + self.results_expressions
            + self.objective_expressions
            + self.constraint_expressions,
        )

        data = data.T.drop_duplicates().T

        return x, f, data

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
            n_samples (int): Number of samples to generate.
            lower_bounds (List[float]): Lower bounds of the design space.
            upper_bounds (List[float]): Upper bounds of the design space.
            nvar (int): Number of design variables.

        Returns:
            List[List[float]]: The samples ready to be evaluated.
        """
        pass


class SamplingProblem:
    def __init__(self, problem_constructor: ProblemConstructor, evaluator: Evaluator):
        """Initialize the sampling problem.

        Args:
            problem_constructor (ProblemConstructor): The problem to be evaluated.
            evaluator (Evaluator): The evaluator to be used.
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
            x (List[List[float]]): Parameters samples.
            out (Dict[str, List[List[float]]]): Retruned dictionary (inspured by Pymoo).

        Returns:
            Dict[str, List[List[float]]]: The evaluated samples, objectives and constraints.
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

        Raises:
            ValueError: If no objective expressions are defined.

        Args:
            problem_constructor (ProblemConstructor): The problem to be evaluated.
            evaluator (Evaluator): The evaluator to be used.
            restart_pop (Union[FloatRandomSampling, Population], optional): A population to restart the optimizer.
        """

        objective_expressions = problem_constructor.get_objectives_expressions()
        if not objective_expressions:  # There have to be objectives.
            raise ValueError("No objective expressions defined.")
        else:
            self.objective_expressions = objective_expressions

        self.problem_constructor = problem_constructor
        self.pname = problem_constructor.get_pnames()
        self.constraint_expressions = problem_constructor.get_constraints_expressions()
        self.results_expressions = evaluator.get_results_request()
        self.evaluator = evaluator
        self.restart_pop = restart_pop

    def optimize(
        self, termination: Tuple[str, int], use_surrogate: bool = False
    ) -> Tuple:
        """Optimize the design.

        Args:
            termination (Tuple[str, int]): A tuple containing the termination criterion as described in Pymoo library.

        Returns:
            Tuple: The samples, the objective values and the results.
        """

        problem = OptimizationProblem(
            self.problem_constructor, self.evaluator, use_surrogate=use_surrogate
        )
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

        data = concatenate([x_hist, r_hist], axis=1)
        data = DataFrame(
            data,
            columns=self.pname
            + self.results_expressions
            + self.objective_expressions
            + self.constraint_expressions,
        )

        data = data.T.drop_duplicates().T  # drop duplicate columns

        return x, f, data

    @abstractmethod
    def _algorithm(self):
        """Implement the optimization algorithm to be used."""
        pass


class OptimizationProblem(ElementwiseProblem):
    def __init__(
        self,
        problem_constructor: ProblemConstructor,
        evaluator: Evaluator,
        use_surrogate: bool = False,
    ):
        """Initialize the optimization problem.

        Args:
            problem_constructor (ProblemConstructor): The problem to be evaluated.
            evaluator (Evaluator): The evaluator to be used.
        """

        self._use_surrogate = use_surrogate
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

    def _evaluate(self, x, out: dict, *args, **kwargs):
        """Evaluate the optimization problem on the given designs.

        Args:
            x (_type_): Design samples.
            out (dict): dictionary containing the evaluated samples, objectives and constraints.
        """

        parameters = {name: value for name, value in zip(self._pnames, x)}
        results = self._evaluator.evaluate(
            parameters, use_surrogate=self._use_surrogate
        )

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
