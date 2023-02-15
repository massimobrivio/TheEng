from collections import defaultdict
from typing import Callable, Dict, List

from abstract import Blues
from numpy import concatenate
from pandas import DataFrame
from problem import ProblemConstructor
from samplers import Samplers
from scipy.stats import qmc


class Sampler(Blues):
    def __init__(
        self,
        problem: ProblemConstructor,
        evaluator: Callable[[Dict[str, float]], Dict[str, float]],
    ) -> None:
        super().__init__(problem, evaluator)

    def do(self, samplerName: str, nSamples: int):
        problem = SamplingProblem(self.problem, self.evaluator)

        samplerMethod = self._getGreen(Samplers, samplerName, nVar=self.nVar)()
        samp = samplerMethod.random(n=nSamples)
        x = qmc.scale(samp, self.lowerBounds, self.upperBounds).tolist()

        out = defaultdict(list)
        res = problem._evaluate(x, out)  # type: ignore

        f = res["F"]
        r = res["R"]

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


class SamplingProblem:
    def __init__(
        self,
        problem: ProblemConstructor,
        evaluator: Callable[[Dict[str, float]], Dict[str, float]],
    ):
        """Initialize the sampling problem.

        Args:
            problem (ProblemConstructor): The problem to be evaluated.
            evaluator (Evaluator): The evaluator to be used.
        """
        self._evaluator = evaluator

        self._nVar = problem.getNvar()
        self._pnames = problem.getPnames()

        self._objectives = problem.getObjectives()
        self._constraints = problem.getConstraints()
        self._lowerBounds, self._upperBounds = problem.getBounds()

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
            results = self._evaluator(parameters)

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


if __name__ == "__main__":
    from simulator import Simulator

    problem = ProblemConstructor()
    problem.setObjectives(["Disp^2"])
    problem.setContraints(["Disp-2"])
    problem.setBounds(
        {"Length": (2000, 5000), "Width": (1000, 3000), "Height": (500, 1500)}
    )
    problem.setResults(["Disp"])

    simul = Simulator()
    simulator = simul.do(
        "femSimulator",
        "examples\\beam_freecad\\FemCalculixCantilever3D_Param.FCStd",
        ["Disp"],
    )

    sampler = Sampler(problem, simulator)
    samples, f, data = sampler.do("latinHypercube", 5)

    print(data)
