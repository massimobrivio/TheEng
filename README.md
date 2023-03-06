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

Here is illustrated a simple usage for minimizing the maximum displacement of a beam while minimizing the maximum stress of it.

The parameters are (*Length*, *Width*, *Height*) of the beam.

```python
from os.path import join

from optimizer import Optimizer
from pandas import concat
from ranker import Ranker
from sampler import Sampler
from simulator import Simulator
from visualization import Visualization


problem = ProblemConstructor()
problem.setResults(
    {
        "Disp": "Max", 
        "Stress": "Max", 
        "Length": None
        }
)
problem.setObjectives(["-Disp", "Stress"])
problem.setContraints(["3000 - Length"])
problem.setBounds(
    {
        "Length": (2000, 5000), 
        "Width": (1000, 3000), 
        "Height": (500, 1500)
        }
)

simul = Simulator(problem)
simulator = simul.do(
    simulatorName="femSimulator",
    fcdPath="examples\\beam_freecad_multiobj\\FemCalculixCantilever3D_Param.FCStd",
)

sampler = Sampler(problem, simulator)
xSamp, fSamp, dataSamp = sampler.do(
    samplerName="latinHypercube", 
    nSamples=10
)

surrog = Surrogate(problem, dataSamp)
surrogate, surrogatePerformance = surrog.do(
    surrogateName="polynomial", 
    save=True, 
    degree_fit=3, 
    surrogatePath="surrogate.pkl"
)

optimizer = Optimizer(problem, surrogate)
xOpt, fOpt, dataOptSur = optimizer.do(
    optimizerName="nsga3", 
    termination=("n_eval", 200), 
    popSize=10

)
xOpt, fOpt, dataOpt = optimizer.convertToSimulator(x=xOpt, simulator=simulator)

ranker = Ranker(
    problem,
    data=concat([dataSamp, dataOpt]),
    weights=(0.6, 0.4),
    constraintsRelaxation=[30,],
)
dataRanked = ranker.do(
    rankingName="simpleAdditive"
)

print("Ranked results are: \n", dataRanked)

visualizer = Visualization(dataRanked)
visualizer.do(
    visualizationName="parallelCoordinate", 
    savePath="parallel_coord.html"
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