from theeng.interfaces.analytical_interface import AnalyticalInterface
from funcs import objective
from theeng.utilities.types import Parameter, Target
from theeng.aidev import AiDev
from theeng.utilities.types import FeatureDefinition
from theeng.blocks.postprocessing import ScatterPlot, ParallelCoord
from os.path import join
from os import getcwd


if __name__ == "__main__":
    path = join(getcwd(), "examples", "multiobjective")
    parameters = [
        Parameter("x1", -2.0, 2.0),
        Parameter("x2", -2.0, 2.0),
    ]
    targets = [
        Target("f1", weight=0.5, ineq=5, is_objective=True, is_constraint=True),
        Target("f2", weight=0.5, ineq=2000, is_objective=True, is_constraint=True),
    ]

    features = FeatureDefinition(parameters, targets)
    anal = AnalyticalInterface(objective, features)

    ai = AiDev(
        features,
        anal.objective,
        path=path,
    )

    ai.sampling_strategy = "latin"
    ai.n_samples = 64

    ai.optimization_strategy = "global"
    ai.popsize = 10
    ai.global_iter = 2
    ai.local_iter = 100

    ai.surrogate_strategy = "polynomial"
    ai.degree_fit = 2
    ai.interaction_only = False
    ai.fit_intercept = True

    data = ai.run(restart=True)

    ScatterPlot(
        data,
        pareto_x="f1",
        pareto_y="f2",
        save=True,
        figname=join(path, "pareto.html"),
    )
    ParallelCoord(data, save=True, figname=join(path, "parallelcoord.html"))

    print(data[data["efficiency"] == "Efficient"])
