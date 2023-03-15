from os import getcwd
from os.path import join

from theeng.core.optimizer import Optimizer
from theeng.core.problem import ProblemConstructor
from theeng.core.ranker import Ranker
from theeng.core.visualization import Visualization


def simulator(parameters):
    x1 = parameters["x1"]
    x2 = parameters["x2"]
    results = {}
    results["f1"] = 100 * (x1**2 + x2**2)
    results["f2"] = (x1 - 1) ** 2 + x2**2
    results["x1"] = x1
    results["x2"] = x2
    return results


if __name__ == "__main__":
    wd = join(getcwd(), "examples", "pymoo_analytical_multiobj")

    problem = ProblemConstructor()
    problem.setResults({"f1": None, "f2": None, "x1": None, "x2": None})
    problem.setObjectives({"f1": 0.5, "f2": 0.5})
    problem.setContraints(
        {
            "11.1111*x1^2 - 11.1111*x1 + 1": 20.0,  # expanded from 2*(x[0]-0.1) * (x[0]-0.9) / 0.18
            "-4.16667*x1^2 + 4.16667*x1 - 1": 20.0,  # expanded from - 20*(x[0]-0.4) * (x[0]-0.6) / 4.8
        },
    )
    problem.setBounds({"x1": (-2, 2), "x2": (-2, 2)})

    optimizer = Optimizer(problem, simulator)
    xOpt, fOpt, dataOpt = optimizer.optimize(
        optimizerName="nsga3", termination=("n_eval", 1600), popSize=40
    )

    ranker = Ranker(problem, dataOpt)
    dataRanked = ranker.rank(rankingName="simpleAdditive")

    dataRanked.to_csv(join(wd, "db.csv"))

    print("Ranked results are: \n", dataRanked)

    visualizer = Visualization(dataRanked)
    visualizer.plot(
        visualizationName="scatterPlot",
        savePath=join(wd, "scatter.html"),
        xName="f1",
        yName="f2",
    )
    visualizer.plot(
        visualizationName="parallelCoordinate", savePath=join(wd, "parallel_coord.html")
    )
    visualizer.plot(visualizationName="heatMap", savePath=join(wd, "heatmap.html"))
