from os import getcwd
from os.path import join
import cProfile
import pstats

from pandas import concat

from theeng.core.optimizer import Optimizer
from theeng.core.problem import ProblemConstructor
from theeng.core.ranker import Ranker
from theeng.core.sampler import Sampler
from theeng.core.simulator import Simulator
from theeng.core.surrogate import Surrogate
from theeng.core.visualization import Visualization

if __name__ == "__main__":
    with cProfile.Profile() as profile:
        wd = join(getcwd(), "examples", "beam_freecad_multiobj_surrogate")

        problem = ProblemConstructor()
        problem.setResults({"Disp": "Max", "Stress": "Max", "Length": None})
        problem.setObjectives(["-Disp", "Stress"])
        problem.setContraints(["3000 - Length"])
        problem.setBounds(
            {"Length": (2000, 5000), "Width": (1000, 3000), "Height": (500, 1500)}
        )

        simul = Simulator(problem)
        simulator = simul.do(
            simulatorName="femSimulator",
            fcdPath=join(wd, "FemCalculixCantilever3D_Param.FCStd"),
        )

        sampler = Sampler(problem, simulator)
        xSamp, fSamp, dataSamp = sampler.do(samplerName="latinHypercube", nSamples=20)

        surrog = Surrogate(problem, dataSamp)
        surrogate, surrogatePerformance = surrog.do(
            surrogateName="polynomial",
            save=True,
            degree_fit=3,
            surrogatePath=join(wd, "surrogate.pkl"),
        )

        optimizer = Optimizer(problem, surrogate)
        xOpt, fOpt, dataOptSur = optimizer.do(
            optimizerName="nsga3", termination=("n_eval", 200), popSize=10
        )

        xOpt, fOpt, dataOpt = optimizer.convertToSimulator(xOpt, simulator)

        ranker = Ranker(
            problem,
            concat([dataSamp, dataOpt]),
            weights=(0.5, 0.5),
            constraintsRelaxation=[
                30,
            ],
        )
        dataRanked = ranker.do(rankingName="simpleAdditive")

        print("Ranked results are: \n", dataRanked)

        visualizer = Visualization(dataRanked)
        visualizer.do(
            visualizationName="scatterPlot",
            savePath=join(wd, "scatter.html"),
            xName="Disp",
            yName="Stress",
        )
        visualizer.do(
            visualizationName="parallelCoordinate", savePath=join(wd, "parallel_coord.html")
        )
        visualizer.do(visualizationName="heatMap", savePath=join(wd, "heatmap.html"))

    stream = open(join(wd, 'output.txt'), 'w')
    results = pstats.Stats(profile, stream=stream)
    results.sort_stats(pstats.SortKey.TIME)
    results.print_stats()