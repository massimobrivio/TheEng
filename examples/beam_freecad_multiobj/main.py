from os import getcwd
from os.path import join

from theeng.core.optimizer import Optimizer
from theeng.core.problem import ProblemConstructor
from theeng.core.ranker import Ranker
from theeng.core.simulator import Simulator
from theeng.core.visualization import Visualization

if __name__ == "__main__":
    wd = join(getcwd(), "examples", "beam_freecad_multiobj")

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

    optimizer = Optimizer(problem, simulator)
    xOpt, fOpt, dataOpt = optimizer.do(
        optimizerName="nsga3", termination=("n_eval", 30), popSize=5
    )

    ranker = Ranker(
        problem,
        dataOpt,
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