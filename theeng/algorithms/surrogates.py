from typing import Tuple

from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.linear_model import LinearRegression
from sklearn.neural_network import MLPRegressor
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import PolynomialFeatures, SplineTransformer, StandardScaler
from sklearn.svm import SVR


class Surrogates:
    def __init__(self) -> None:
        pass

    def polynomial(
        self,
        degree_fit: int = 2,
        interaction_only: bool = False,
        fit_intercept: bool = True,
        **kwargs
    ) -> Pipeline:
        """_summary_

        Args:
            degree_fit (int, optional): The degree of the fitting polynomial. Defaults to 2.
            interaction_only (bool, optional): If to consider design variable interactions. Defaults to False.
            fit_intercept (bool, optional): Whether to fit the intercept. Defaults to True.

        Returns:
            Pipeline: A Scikit-Learn pipeline.
        """
        pipeline = Pipeline(
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

        return pipeline

    def gaussianProcess(self, kernel=None, **kwargs) -> Pipeline:
        """_summary_

        Args:
            kernel (_type_, optional): Kernel for the Gauss process. Defaults to None.

        Returns:
            Pipeline: A Scikit-Learn pipeline.
        """
        pipeline = Pipeline(
            [
                ("scaler", StandardScaler()),
                (
                    "gauss",
                    GaussianProcessRegressor(kernel=kernel, n_restarts_optimizer=10, random_state=0),
                ),
            ]
        )

        return pipeline

    def neuralNetwork(
        self,
        n_nodes: Tuple[int, int] = (16, 8),
        activation: str = "relu",
        solver: str = "adam",
        n_epochs: int = 1000,
        **kwargs
    ) -> Pipeline:
        """_summary_

        Args:
            n_nodes (Tuple[int, int], optional): NUmber of nodes in each layer. Defaults to (16, 8).
            activation (str, optional): Activation function for the NN. Defaults to "relu".
            solver (str, optional): The backpropagation optimizer. Defaults to "adam".
            n_epochs (int, optional): The number of epochs. Defaults to 1000.

        Returns:
            Pipeline: A Scikit-Learn pipeline.
        """
        pipeline = Pipeline(
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

        return pipeline

    def supportVector(
        self, kernel: str = "rbf", degree_fit: int = 2, **kwargs
    ) -> Pipeline:
        """_summary_

        Args:
            kernel (str, optional): The Kernel of the SVM. Defaults to "rbf".
            degree_fit (int, optional): The degree of the fitting polynomial. Defaults to 2.

        Returns:
            Pipeline: A Scikit-Learn pipeline.
        """
        pipeline = Pipeline(
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

        return pipeline

    def spline(
        self,
        n_knots: int = 2,
        degree_fit: int = 2,
        fit_intercept: bool = True,
        **kwargs
    ) -> Pipeline:
        """_summary_

        Args:
            n_knots (int, optional): Number of spline knots. Defaults to 2.
            degree_fit (int, optional): The degree of the fitting polynomial. Defaults to 2.
            fit_intercept (bool, optional): Whether to fit the intercept. Defaults to True.

        Returns:
            Pipeline: A Scikit-Learn pipeline.
        """
        pipeline = Pipeline(
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

        return pipeline
