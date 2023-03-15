import json
from os.path import isfile, join

from pandas import concat

from theeng.core.sampler import Sampler
from theeng.core.simulator import Simulator
from theeng.core.surrogate import Surrogate
from theeng.core.optimizer import Optimizer
from theeng.core.problem import ProblemConstructor
from theeng.core.ranker import Ranker
from theeng.core.visualization import Visualization


class TheEng:
    def __init__(
        self, makeSampling=True, makeSurrogate=True, makeOptimization=True
    ) -> None:
        self.makeSampling = makeSampling
        self.makeSurrogate = makeSurrogate
        self.makeOptimization = makeOptimization

        self.settingsReady = False

        self.workingDirectory = ""
        self.simulationDirectory = ""
        self.nCPUs = None
        self.bounds = None
        self.samplerName = ""
        self.nSamples = None
        self.surrogateName = ""
        self.degree_fit = None
        self.fit_intercept = None
        self.fit_interactions = None
        self.optimizerName = ""
        self.popSize = None
        self.termination = None
        self.objectivesExpressions = None
        self.constraintsExpressions = None

    def run(self):
        if not self.settingsReady:
            raise Exception(
                "Settings are not ready. Please run getInputsFromJson() method first."
            )
        problem = ProblemConstructor()
        problem.setResults({"f1": None, "f2": None, "x1": None, "x2": None})
        problem.setObjectives(["f1", "f2"])
        problem.setContraints(
            [
                "11.1111*x1^2 - 11.1111*x1 + 1",  # expanded from 2*(x[0]-0.1) * (x[0]-0.9) / 0.18
                "-4.16667*x1^2 + 4.16667*x1 - 1",  # expanded from - 20*(x[0]-0.4) * (x[0]-0.6) / 4.8
            ],
        )
        problem.setBounds({"x1": (-2, 2), "x2": (-2, 2)})

        simul = Simulator(problem)
        simulator = simul.generate(
            simulatorName="femSimulator",
            fcdPath=join(self.workingDirectory, "FemCalculixCantilever3D_Param.FCStd"),
        )

        sampler = Sampler(problem, simulator)
        _, _, dataSamp = sampler.sample(nSamples=50)

        surrog = Surrogate(problem, dataSamp)
        surrogate, _ = surrog.generate(
            surrogateName="polynomial",
            save=True,
            degree_fit=1,
            surrogatePath=join(self.workingDirectory, "surrogate.pkl"),
        )

        optimizer = Optimizer(problem, surrogate)
        xOpt, fOpt, dataOpt = optimizer.optimize(
            optimizerName="nsga3", termination=("n_eval", 1600), popSize=40
        )

        _, _, dataOpt = optimizer.convertToSimulator(xOpt, simulator)

        ranker = Ranker(
            problem,
            concat([dataSamp, dataOpt]),
            weights=(0.5, 0.5),
            constraintsRelaxation=[20, 20],
        )
        dataRanked = ranker.rank(rankingName="simpleAdditive")

        dataRanked.to_csv(join(self.workingDirectory, "db.csv"))

        visualizer = Visualization(dataRanked)
        visualizer.plot(
            visualizationName="scatterPlot",
            savePath=join(self.workingDirectory, "scatter.html"),
            xName="f1",
            yName="f2",
        )
        visualizer.plot(
            visualizationName="parallelCoordinate",
            savePath=join(self.workingDirectory, "parallel_coord.html"),
        )
        visualizer.plot(
            visualizationName="heatMap",
            savePath=join(self.workingDirectory, "heatmap.html"),
        )

    def getInputsFromJson(self, jsonPath):
        self._checkFileExists(jsonPath)
        with open(jsonPath, "r") as f:
            self._inputs = json.load(f)

        self._getGeneralSettings()
        self._getProblemSettings()

        if self.makeSampling:
            self._getSamplingSettings()
        if self.makeSurrogate:
            self._getSurrogateSettings()
        if self.makeOptimization:
            self._getOptimizationSettings()

        self.settingsReady = True

    def _getGeneralSettings(self):
        generalSettings = self._inputs["General Settings"]
        self.workingDirectory = generalSettings["Working Directory"]
        self.simulationDirectory = generalSettings["Simulation Directory"]
        self.nCPUs = generalSettings["nCPUs"]

    def _getProblemSettings(self):
        problemSettings = self._inputs["Problem"]
        self.bounds = problemSettings["Parameters"]

    def _getSamplingSettings(self):
        samplingSettings = self._inputs["Sampling"]
        self.samplerName = samplingSettings["Method"]
        self.nSamples = samplingSettings["Number of Samples"]

    def _getSurrogateSettings(self):
        surrogateSettings = self._inputs["Surrogate"]
        self.surrogateName = surrogateSettings["Method"]
        self.degree_fit = surrogateSettings["Degree of Fit"]
        self.fit_intercept = surrogateSettings["Fit Intercept"]
        self.fit_interactions = surrogateSettings["Fit Interactions"]

    def _getOptimizationSettings(self):
        optimizationSettings = self._inputs["Optimization"]
        self.optimizerName = optimizationSettings["Method"]
        self.popSize = optimizationSettings["Population Size"]
        n_eval = optimizationSettings["Number of Evaluations"]
        self.termination = ("n_eval", n_eval)
        self.objectivesExpressions = list(
            optimizationSettings["Objectives Expressions"].keys()
        )
        self.constraintsExpressions = list(
            optimizationSettings["Constraints Expressions"].keys()
        )

    # check if file exists
    def _checkFileExists(self, filePath):
        if not isfile(filePath):
            raise FileNotFoundError(
                "Input json file does not exist. Check path and try again."
            )
