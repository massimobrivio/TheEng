from typing import Tuple

from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.linear_model import LinearRegression
from sklearn.neural_network import MLPRegressor
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import PolynomialFeatures, SplineTransformer, StandardScaler
from sklearn.svm import SVR


class Surrogate:
    def polynomial(
        self,
        degree_fit: int = 2,
        interaction_only: bool = False,
        fit_intercept: bool = True,
    ) -> Pipeline:
        pipe = Pipeline(
            [
                ("scaler", StandardScaler()),
                (
                    "poly",
                    PolynomialFeatures(
                        degree=degree_fit,
                        interaction_only=interaction_only,
                    ),
                ),
                (
                    "linear",
                    LinearRegression(fit_intercept=fit_intercept),
                ),
            ]
        )
        return pipe

    def gaussian_process(self, kernel=None) -> Pipeline:
        pipe = Pipeline(
            [
                ("scaler", StandardScaler()),
                (
                    "gauss",
                    GaussianProcessRegressor(kernel=kernel, random_state=0),
                ),
            ]
        )
        return pipe

    def neural_network(
        self,
        n_nodes: Tuple[int, int] = (16, 8),
        activation: str = "relu",
        solver: str = "adam",
        n_epochs: int = 1000,
    ) -> Pipeline:
        pipe = Pipeline(
            [
                ("scaler", StandardScaler()),
                (
                    "mlp",
                    MLPRegressor(
                        hidden_layer_sizes=n_nodes,
                        activation=activation,
                        solver=solver,
                        max_iter=n_epochs,
                        early_stopping=True,
                    ),
                ),
            ]
        )
        return pipe

    def support_vector_machine(
        self, kernel: str = "rbf", degree_fit: int = 2
    ) -> Pipeline:
        pipe = Pipeline(
            [
                ("scaler", StandardScaler()),
                (
                    "svr",
                    SVR(
                        kernel=kernel,
                        degree=degree_fit,
                    ),
                ),
            ]
        )
        return pipe

    def spline(
        self, n_knots: int = 2, degree_fit: int = 2, fit_intercept: bool = True
    ) -> Pipeline:
        pipe = Pipeline(
            [
                ("scaler", StandardScaler()),
                (
                    "spline",
                    SplineTransformer(
                        n_knots=n_knots,
                        degree=degree_fit,
                    ),
                ),
                (
                    "linear",
                    LinearRegression(fit_intercept=fit_intercept),
                ),
            ]
        )
        return pipe
