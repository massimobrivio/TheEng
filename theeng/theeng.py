import json
from os.path import isfile, join

from pandas import concat

from theeng.core.optimizer import Optimizer
from theeng.core.problem import ProblemConstructor
from theeng.core.ranker import Ranker
from theeng.core.sampler import Sampler
from theeng.core.simulator import Simulator
from theeng.core.surrogate import Surrogate
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
        self.simulatorName = ""
        self.nCPUs = None
        self.results = None
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
        self.rankingName = ""
        self.objectives = None
        self.objectiveWeights = None
        self.constraints = None
        self.constraintsRelaxations = None

    def run(self):
        if not self.settingsReady:
            raise Exception(
                "Settings are not ready. Please run getSettingsFromDict() or getSettingsFromJson() method first."
            )
        problem = ProblemConstructor()
        problem.setResults(self.results)
        problem.setObjectives(self.objectives)
        problem.setContraints(self.constraints)
        problem.setBounds(self.bounds)

        simul = Simulator(problem)
        simulator = simul.generate(
            simulatorName=self.simulatorName,
            fcdPath=self.simulationDirectory,
        )

        if self.makeSampling:
            sampler = Sampler(problem, simulator)
            _, _, dataSamp = sampler.sample(nSamples=self.nSamples)

        if self.makeSurrogate and self.makeSampling:
            surrog = Surrogate(problem, dataSamp)
            surrogate, _ = surrog.generate(
                surrogateName=self.surrogateName,
                save=True,
                degree_fit=self.degree_fit,
                surrogatePath=join(self.workingDirectory, "surrogate.pkl"),
            )

        if self.makeOptimization:
            optimizer = Optimizer(problem, surrogate)
            xOpt, _, dataOpt = optimizer.optimize(
                optimizerName=self.optimizerName, termination=self.termination, popSize=self.popSize
            )
            if self.makeSurrogate:
                _, _, dataOpt = optimizer.convertToSimulator(xOpt, simulator)

        if self.makeSampling and self.makeOptimization:
            data = concat([dataSamp, dataOpt])
        elif self.makeSampling:
            data = dataSamp
        elif self.makeOptimization:
            data = dataOpt

        ranker = Ranker(problem, data)
        dataRanked = ranker.rank(rankingName=self.rankingName)

        dataRanked.to_csv(join(self.workingDirectory, "db.csv"))

        visualizer = Visualization(dataRanked)

        visualizer.plot(
            visualizationName="parallelCoordinate",
            savePath=join(self.workingDirectory, "parallel_coord.html"),
        )
        visualizer.plot(
            visualizationName="heatMap",
            savePath=join(self.workingDirectory, "heatmap.html"),
        )

    def getSettingsFromJson(self, jsonPath):
        self._checkFileExists(jsonPath)
        with open(jsonPath, "r") as f:
            self._settings = json.load(f)
        self.getSettingsFromDict(self._settings)

    def getSettingsFromDict(self, settings):
        self._settings = settings

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
        generalSettings = self._settings["General Settings"]
        self.workingDirectory = generalSettings["Working Directory"]
        self.simulationDirectory = generalSettings["Simulation Directory"]
        self.simulatorName = generalSettings["Simulator Name"]
        self.nCPUs = generalSettings["nCPUs"]

    def _getProblemSettings(self):
        problemSettings = self._settings["Problem"]
        self.bounds = problemSettings["Parameters"]
        self.results = {}
        for resultName, resultOperation in problemSettings["Results"].items():
            if resultOperation == "None":
                resultOperation = None
            self.results[resultName] = resultOperation

    def _getSamplingSettings(self):
        samplingSettings = self._settings["Sampling"]
        self.samplerName = samplingSettings["Method"]
        self.nSamples = samplingSettings["Number of Samples"]

    def _getSurrogateSettings(self):
        surrogateSettings = self._settings["Surrogate"]
        self.surrogateName = surrogateSettings["Method"]
        self.degree_fit = surrogateSettings["Degree of Fit"]
        self.fit_intercept = surrogateSettings["Fit Intercept"]
        self.fit_interactions = surrogateSettings["Fit Interactions"]

    def _getOptimizationSettings(self):
        optimizationSettings = self._settings["Optimization"]
        self.optimizerName = optimizationSettings["Method"]
        self.popSize = optimizationSettings["Population Size"]
        n_eval = optimizationSettings["Number of Evaluations"]
        self.termination = ("n_eval", n_eval)
        self.rankingName = optimizationSettings["Ranking Method"]
        self.objectives = optimizationSettings["Objectives Expressions"]
        self.constraints = optimizationSettings["Constraints Expressions"]

    # check if file exists
    def _checkFileExists(self, filePath):
        if not isfile(filePath):
            raise FileNotFoundError(
                "Input json file does not exist. Check path and try again."
            )
