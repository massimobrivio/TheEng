from scipy.stats.qmc import LatinHypercube


class Samplers:
    def __init__(self, nVar) -> None:
        self.nVar = nVar

    def latinHypercube(self) -> LatinHypercube:
        sampler = LatinHypercube(d=self.nVar)
        return sampler
