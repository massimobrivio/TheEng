from funcs import objective
from theeng.interfaces.analytical_interface import AnalyticalInterface
from theeng.utilities.types import Parameter, Target
from theeng.blocks.postprocessing import HeatMap, ScatterPlot
from theeng.utilities.types import FeatureDefinition
from theeng.aidev import AiDev
from os.path import join
from os import getcwd


if __name__ == "__main__":

    path = join(getcwd(), "examples", "beam")

    x1 = Parameter("x1", 200, 400)
    x2 = Parameter("x2", 10, 40)
    x3 = Parameter("x3", 10, 40)
    f1 = Target("f1", weight=1, ineq=0.1)
    parameters = [x1, x2, x3]
    targets = [f1]
    features = FeatureDefinition(parameters, targets)
    anal = AnalyticalInterface(objective, features)

    ai = AiDev(
        features,
        anal.objective,
        path=path,
    )
    ai.optimization_strategy = "local"
    ai.global_optimizer = "PSO"

    data = ai.run(restart=True)

    HeatMap(data, save=True, figname=join(path, "heatmap.html"))
    ScatterPlot(
        data,
        pareto_x="x3",
        pareto_y="f1",
        save=True,
        figname=join(path, "pareto.html"),
    )

    print(data[data["efficiency"] == "Efficient"])
