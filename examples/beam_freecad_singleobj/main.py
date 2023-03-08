from os import getcwd
from os.path import join

from theeng.core.optimizer import Optimizer
from theeng.core.problem import ProblemConstructor
from theeng.core.ranker import Ranker
from theeng.core.simulator import Simulator
from theeng.core.visualization import Visualization

if __name__ == "__main__":
    wd = join(getcwd(), "examples", "beam_freecad_singleobj")

    problem = ProblemConstructor()
    problem.setResults({"Disp": "Max", "Length": None})
    problem.setObjectives(["Disp"])
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
        optimizerName="nelderMead", termination=("n_eval", 30)
    )

    ranker = Ranker(
        problem,
        dataOpt,
        weights=(1, ),
        constraintsRelaxation=[
            30,
        ],
    )
    dataRanked = ranker.do(rankingName="simpleAdditive")

    print("Ranked results are: \n", dataRanked)

    visualizer = Visualization(dataRanked)
    visualizer.do(
        visualizationName="parallelCoordinate", savePath=join(wd, "parallel_coord.html")
    )
    visualizer.do(visualizationName="heatMap", savePath=join(wd, "heatmap.html"))
