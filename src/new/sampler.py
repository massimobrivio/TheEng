from samplers import Samplers
from inspect import getmembers, ismethod
from scipy.stats import qmc
from typing import List, Tuple, Dict
from difflib import SequenceMatcher
from problem import ProblemConstructor
from evaluator import Evaluator
from collections import defaultdict
from pandas import DataFrame
from numpy import concatenate


class Sampler:
    def __init__(
        self, problem: ProblemConstructor, evaluator: Evaluator
    ) -> None:
        
        self.problem = problem
        self.evaluator = evaluator
        
        self.pname = problem.getPnames()
        self.objectiveExpressions = problem.getObjectivesExpressions()
        self.constraintExpressions = problem.getConstraintsExpressions()
        self.lowerBounds, self.upperBounds = problem.getBounds()
        self.resultsExpressions = evaluator.getResultsRequest()

        self.nVar = len(self.pname)
        
        self.sampler = None

    def sample(self, samplerName: str, nSamples: int):
        problem = SamplingProblem(self.problem, self.evaluator)

        samplerMethod = self._getSampler(samplerName)()
        samp = samplerMethod.random(n=nSamples)
        samples = qmc.scale(samp, self.lowerBounds, self.upperBounds).tolist()

        out = defaultdict(list)
        res = problem._evaluate(samples, out)  # type: ignore

        f = res["F"]
        r = res["R"]

        data = concatenate([samples, r], axis=1)
        data = DataFrame(
            data,
            columns=self.pname
            + self.resultsExpressions
            + self.objectiveExpressions
            + self.constraintExpressions,
        )

        data = data.T.drop_duplicates().T

        return samples, f, data

    def _getSampler(self, samplerName: str):
        samplers = Samplers(self.nVar)
        availableSamplers = [m[0] for m in getmembers(samplers, predicate=ismethod)]
        if samplerName not in availableSamplers:
            similarMethods, similarity_ratio = Sampler._findSimilar(
                samplerName, availableSamplers
            )
            similarMethod = similarMethods[0]
            print(
                f"Method {samplerName} not available or misspelled. Using {similarMethod} instead.\n Matching percentage: {round(similarity_ratio[0]*100, 2)} %"
            )
            samplerName = similarMethod  # overwrite method with similar method
        samplerMethod = getattr(samplers, samplerName)
        return samplerMethod

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


class SamplingProblem:
    def __init__(self, problem: ProblemConstructor, evaluator: Evaluator):
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
    simulator = simul.generate("femSimulator", "examples\\beam_freecad\\FemCalculixCantilever3D_Param.FCStd", ["Disp"])
    
    evaluator = Evaluator(["Disp"])
    evaluator.setSimulator(simulator)
    
    sampler = Sampler(problem, evaluator)
    samples, f, data = sampler.sample("latinHypercube", 5)
    
    print(data)
    
    
    