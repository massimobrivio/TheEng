from abc import ABC, abstractmethod
from collections import defaultdict
from typing import Callable, Dict, Iterable, List, Tuple, Union

from numpy import concatenate
from pandas import DataFrame
from plotly.graph_objects import Figure
from pymoo.core.population import Population
from pymoo.core.callback import Callback
from pymoo.core.problem import ElementwiseProblem
from pymoo.operators.sampling.rnd import FloatRandomSampling
from pymoo.optimize import minimize
from sklearn.model_selection import cross_val_score
from sklearn.pipeline import Pipeline


class Target:
    """
    Class for defining a target variable.
    """

    def __init__(
        self,
        name: str,
        weight: float,
        ineq: float,
        is_objective: bool = True,
        is_minimization: bool = True,
        is_constraint: bool = False,
        is_measurement: bool = False,
    ) -> None:
        """_summary_

        Args:
            name (str): _description_
            weight (float): _description_
            ineq (float): _description_
            is_objective (bool): _description_
            is_constraint (bool): _description_
            is_measurement (bool): _description_

        """
        self.name = name
        self.weight = float(weight)
        self.ineq = None
        self.is_constraint = is_constraint
        if self.is_constraint:
            self.ineq = float(ineq) if isinstance(ineq, int) else ineq
        self.is_objective = is_objective
        self.is_measurements = is_measurement
        self.is_minimization = is_minimization

    def __repr__(self) -> str:
        return f"Target('{self.name}', {self.weight}, {self.ineq}, {self.is_objective}, {self.is_minimization}, {self.is_constraint}, {self.is_measurements})"


class Parameter:
    """
    Class for defining a parameter variable.
    """

    def __init__(self, name: str, lb: float, ub: float) -> None:
        """_summary_

        Args:
            name (str): _description_
            lb (float): _description_
            ub (float): _description_
        """
        self.name = name
        self.lb = float(lb)
        self.ub = float(ub)

    def __repr__(self) -> str:
        return f"Parameter('{self.name}', {self.lb}, {self.ub})"


class FeatureDefinition:
    """
    Class used to combined and extract parameters and targets related information.

    """

    def __init__(self, parameters: List[Parameter], targets: List[Target]) -> None:
        """_summary_

        Args:
            parameters (List[Parameter]): _description_
            targets (List[Target]): _description_
        """
        self.parameters = parameters
        self.targets = targets
        self._update()

    def _update(self) -> None:
        """
        Update calculated and extracted values from parameters and targets.

        """
        self.pnames = []
        self.lbs = defaultdict(float)
        self.ubs = defaultdict(float)
        self.nvar = len(self.parameters)

        for parameter in self.parameters:
            self.pnames.append(parameter.name)
            self.lbs[parameter.name] = parameter.lb
            self.ubs[parameter.name] = parameter.ub

        self.tnames = []
        self.weights = defaultdict(float)
        self.are_objective = defaultdict(bool)
        self.are_minimizations = defaultdict(bool)
        self.are_constraints = defaultdict(bool)
        self.are_measurements = defaultdict(bool)
        self.ineqs = dict()

        for target in self.targets:
            self.tnames.append(target.name)
            self.weights[target.name] = target.weight
            self.are_objective[target.name] = target.is_objective
            self.are_minimizations[target.name] = target.is_minimization
            self.are_constraints[target.name] = target.is_constraint
            self.are_measurements[target.name] = target.is_measurements
            self.ineqs[target.name] = target.ineq

        assert any(
            list(self.are_objective.values())
        ), "At least one target should be an objective."
        assert len(self.targets) >= 1, "You should specify one or more targets."
        assert len(self.parameters) >= 1, "You should specify one or more parameters."
        assert all(
            [w >= 0 for w in self.weights.values()]
        ), "Weights should all be positive."

        self.nobjs = sum(self.are_objective.values())
        self.nconstrs = sum(self.are_constraints.values())


class Sampling(ABC):
    """
    Abstract class for DoE sampling.
    """

    def __init__(self, features: FeatureDefinition) -> None:
        """_summary_

        Args:
            features (FeatureDefinition): _description_
        """
        self.features = features
        self.lbs = list(features.lbs.values())
        self.ubs = list(features.ubs.values())
        self.nvar = features.nvar

    def __call__(self, n_samples: int = 50) -> DataFrame:
        """_summary_

        Args:
            n_samples (int, optional): _description_. Defaults to 50.

        Returns:
            DataFrame: _description_
        """
        samples = self._method(n_samples)
        return samples

    @abstractmethod
    def _method(self, n_samples: int = 50) -> DataFrame:
        """_summary_

        Args:
            n_samples (int, optional): _description_. Defaults to 50.

        Returns:
            DataFrame: _description_
        """
        pass


class Surrogate(ABC):
    """
    Abstract class for surrogate modelling.
    """

    def __call__(
        self, data: DataFrame, features: FeatureDefinition
    ) -> Tuple[Callable[..., List[float]], Tuple[float, float]]:
        """_summary_

        Args:
            data (DataFrame): _description_
            features (FeatureDefinition): _description_

        Returns:
            Tuple[Callable[..., List[float]], Tuple[float, float]]: _description_
        """

        x = data[features.pnames].values
        y = data[features.tnames].values

        pipe = self._model()
        model = pipe.fit(x, y)
        scores = cross_val_score(model, x, y, cv=4)
        performance = (scores.mean(), scores.std())

        def sur(x: List[float]) -> List[float]:
            return model.predict([x])[0]

        return sur, performance

    @abstractmethod
    def _model(self) -> Pipeline:
        """_summary_

        Returns:
            Pipeline: _description_
        """
        pass


class Optimization(ABC):
    def __init__(
        self,
        objective: Callable[..., List[float]],
        features: FeatureDefinition,
        popsize: int = 10,
        restart_pop: Union[FloatRandomSampling, Population] = FloatRandomSampling(),
    ) -> None:
        """_summary_

        Args:
            objective (Callable[..., List[float]]): _description_
            features (FeatureDefinition): _description_
            popsize (int, optional): _description_. Defaults to 10.
        """
        self.objective = objective
        self.features = features
        self.popsize = int(popsize)
        self.restart_pop = restart_pop

    def __call__(
        self,
        termination: Tuple[str, int],
    ) -> Dict[str, DataFrame]:
        """_summary_

        Args:
            termination (Tuple[str, int]): _description_

        Returns:
            Dict[str, DataFrame]: _description_
        """

        problem = self._problem()
        algorithm = self._algorithm()

        res = minimize(
            problem,
            algorithm,
            termination=termination,
            seed=1,
            callback=HistCallback(),
            return_least_infeasible=True,
        )

        if not isinstance(res.X[0], Iterable):
            res.X = [res.X]
        if not isinstance(res.F[0], Iterable):
            res.F = [res.F]

        x_hist = concatenate(res.algorithm.callback.data["x_hist"])
        rval_hist = concatenate(res.algorithm.callback.data["results"])

        x = DataFrame(res.X, columns=self.features.pnames)

        x_hist = DataFrame(x_hist, columns=self.features.pnames)
        fval_hist = DataFrame(rval_hist, columns=self.features.tnames)

        results = {
            "x": x,
            "x_hist": x_hist,
            "fval_hist": fval_hist,
            "last_pop": res.pop,
        }

        return results

    def _problem(self):
        return Problem(self.objective, self.features)

    @abstractmethod
    def _algorithm(self):
        pass


class Problem(ElementwiseProblem):
    def __init__(
        self,
        objective: Callable[..., List[float]],
        features: FeatureDefinition,
    ) -> None:
        """_summary_

        Args:
            objective (Callable[..., List[float]]): _description_
            nvar (int): _description_
            nobj (int): _description_
            n_ieq_constr (int): _description_
            lbs (list): _description_
            ubs (list): _description_
            ineqs (list): _description_
            are_objs (list): _description_
        """

        self.objective = objective
        self.are_objectives = features.are_objective
        self.are_minimizations = features.are_minimizations
        self.are_constraints = features.are_constraints
        self.ineqs = features.ineqs

        super().__init__(
            n_var=features.nvar,
            n_obj=features.nobjs,
            n_ieq_constr=features.nconstrs,
            xl=list(features.lbs.values()),
            xu=list(features.ubs.values()),
        )

    def _evaluate(self, x, out, *args, **kwargs) -> None:
        """_summary_

        Args:
            x (_type_): _description_
            out (_type_): _description_
        """
        results = self.objective(x)

        f = []
        g = []
        r = []

        for result, ineq, is_obj, is_min, is_consts in zip(
            results,
            self.ineqs.values(),
            self.are_objectives.values(),
            self.are_minimizations.values(),
            self.are_constraints.values(),
        ):
            r.append(result)

            if is_obj:
                if is_min:
                    f.append(result)
                else:
                    f.append(-result)
            if is_consts:
                g.append(result - ineq)

        out["F"] = f
        out["G"] = g
        out[
            "R"
        ] = r  # unmodified results not used for optimization but only for writing to db.csv


class HistCallback(Callback):
    def __init__(self) -> None:
        super().__init__()
        self.data["x_hist"] = []
        self.data["results"] = []

    def notify(self, algorithm):
        self.data["x_hist"].append(algorithm.pop.get("X"))
        self.data["results"].append(algorithm.pop.get("R"))


class Visualization(ABC):
    """
    Abstract class for results visualization.
    """

    def __init__(
        self,
        data: DataFrame,
        save: bool = True,
        figname: str = "results.html",
        **kwargs,
    ):
        """_summary_

        Args:
            data (DataFrame): _description_
            save (bool, optional): _description_. Defaults to True.
            figname (str, optional): _description_. Defaults to "results.html".
        """
        self.fig = self._method(data, **kwargs)
        if save:
            self.fig.write_html(figname)

    def getfig(self):
        return self.fig

    @abstractmethod
    def _method(self, data: DataFrame, **kwargs) -> Figure:
        """_summary_

        Args:
            data (DataFrame): _description_

        Returns:
            Figure: _description_
        """
        pass
