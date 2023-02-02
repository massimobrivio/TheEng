from os import getcwd
from os.path import join

from theeng.aidev import AiDev
from theeng.blocks.postprocessing import ParallelCoord, ScatterPlot, Convergence
from theeng.interfaces.analytical_interface import AnalyticalInterface
from theeng.utilities.types import FeatureDefinition, Parameter, Target

from funcs import objective

if __name__ == "__main__":
    path = join(getcwd(), "examples", "multiobjective_optsampling")
    parameters = [
        Parameter("x1", -2.0, 2.0),
        Parameter("x2", -2.0, 2.0),
    ]
    targets = [
        Target(
            "f2",
            weight=0.5,
            ineq=2000,
            is_objective=True,
            is_minimization=True,
            is_constraint=False,
        ),
        Target(
            "f1",
            weight=0.5,
            ineq=5,
            is_objective=True,
            is_minimization=True,
            is_constraint=False,
        ),
    ]

    features = FeatureDefinition(parameters, targets)
    anal = AnalyticalInterface(objective, features)

    ai = AiDev(
        features,
        anal.objective,
        path=path,
    )

    ai.optimization_strategy = "global"
    ai.popsize = 10
    ai.global_iter = 100

    data = ai.run(sampling=False, surrogate=False, optimization=True, restart=True)

    ScatterPlot(
        data,
        pareto_x="f1",
        pareto_y="f2",
        save=True,
        figname=join(path, "pareto.html"),
    )
    ParallelCoord(data, save=True, figname=join(path, "parallelcoord.html"))
    Convergence(data, features, figname=join(path, "convergence.html"))

    print(data[data["efficiency"] == "Efficient"])
