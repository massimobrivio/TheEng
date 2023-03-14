# TheEng

TheEng is a Python library for dealing with structural optimization.

It is designed to be modular and expandable. It leverages surrogate modelling in order to speed up optimization when function evaluations are too expensive but the optimizer does not assume anything on the objective function, therefore it can directly work on the simulation run (wrapped in a callable).

The library is born for a joint usage together with Finite Element Model (FEM) and parametric CAD modelling but the same workflow can easily be applied to any simulator (e.g. CFD). So far it interface (somehow) with FreeCAD.

The library automates:

1. The sampling of the simulation in order to create a dataset to train the surrogate if needed.
2. The surrogate training.
3. The optimization of the design.
4. The post-processing, using Multi-Criteria Decision Making in order to select the best design.
5. The result visualization.

## Installation

TheEng is available on Pypi.

```bash
pip install -U TheEng
```

## Usage

Here is illustrated a simple usage replicating the example in Pymoo documentation --> [here](https://pymoo.org/getting_started/part_2.html)

The parameters are (*x1*, *x2*).\
The objectives are (*f1*, *f2*).

```python
from os import getcwd
from os.path import join

from theeng.core.optimizer import Optimizer
from theeng.core.problem import ProblemConstructor
from theeng.core.ranker import Ranker
from theeng.core.visualization import Visualization


def simulator(parameters):
    x1 = parameters["x1"]
    x2 = parameters["x2"]
    results = {
        "f1" : 100 * (x1**2 + x2**2)
        "f2" : (x1 - 1) ** 2 + x2**2
        "x1" : x1
        "x2" : x2
    }
    return results


if __name__ == "__main__":
    wd = join(getcwd(), "examples", "pymoo_analytical_multiobj")

    problem = ProblemConstructor()
    problem.setResults({"f1": None, "f2": None, "x1": None, "x2": None})
    problem.setObjectives(["f1", "f2"])
    problem.setContraints(["11.1111*x1^2 - 11.1111*x1 + 1", "-4.16667*x1^2 + 4.16667*x1 - 1",])
    problem.setBounds({"x1": (-2, 2), "x2": (-2, 2)})

    optimizer = Optimizer(problem, simulator)
    xOpt, fOpt, dataOpt = optimizer.optimize(
        optimizerName="nsga3", termination=("n_eval", 1600), popSize=40
    )

    ranker = Ranker(
        problem,
        dataOpt,
        weights=(0.5, 0.5),
        constraintsRelaxation=[20, 20],
    )
    dataRanked = ranker.rank(rankingName="simpleAdditive")

    print("Ranked results are: \n", dataRanked)

    visualizer = Visualization(dataRanked)
    visualizer.plot(
        visualizationName="scatterPlot",
        savePath=join(wd, "scatter.html"),
        xName="f1",
        yName="f2",
    )

```

Results is an interactive html image as below:

![pareto](/images/pareto.png)

## Contributing

The library is in a very initial and exploratory stage. It is a personal way of learning and experimenting.

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[GNU GPLv3 with Commons Clause](https://github.com/massimobrivio/TheEng/blob/main/LICENSE)