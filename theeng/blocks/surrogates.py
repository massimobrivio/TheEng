from typing import Tuple

from theeng.utilities.types import Surrogate
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.linear_model import LinearRegression
from sklearn.neural_network import MLPRegressor
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import PolynomialFeatures, SplineTransformer, StandardScaler
from sklearn.svm import SVR


class Polynomial(Surrogate):
    """
    Class for polynomial regression.
    """

    def __init__(
        self,
        degree_fit: int = 1,
        interaction_only: bool = False,
        fit_intercept: bool = True,
    ) -> None:
        """

        :param degree_fit: Degree of the polynomial.
        :type degree_fit: int
        :param interaction_only: Whether to fit interaction terms
        :type interaction_only: bool
        :param fit_intercept: Whether to fit the intercept
        :type fit_intercept: nool
        """
        self.degree_fit = degree_fit
        self.interaction_only = interaction_only
        self.fit_intercept = fit_intercept

    def _model(self) -> Pipeline:
        """
        Method defining the regressor.

        :return: A sklearn pipeline including scaling of predictors.
        :rtype: Pipeline

        See https://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.PolynomialFeatures.html
        """
        pipe = Pipeline(
            [
                ("scaler", StandardScaler()),
                (
                    "poly",
                    PolynomialFeatures(
                        degree=self.degree_fit,
                        interaction_only=self.interaction_only,
                    ),
                ),
                (
                    "linear",
                    LinearRegression(fit_intercept=self.fit_intercept),
                ),
            ]
        )
        return pipe


class Kriging(Surrogate):
    """
    Class for Kriging regression.
    """

    def __init__(self, kernel=None) -> None:
        """

        :param kernel: Kernel of Gaussian Process (see Sklearn GaussianProcessRegressor docs)
        :type kernel:

        See https://scikit-learn.org/stable/modules/generated/sklearn.gaussian_process.GaussianProcessRegressor.html
        """
        self.kernel = kernel

    def _model(self) -> Pipeline:
        """
        Method defining the regressor.

        :return: A sklearn pipeline including scaling of predictors.
        :rtype: Pipeline
        """
        pipe = Pipeline(
            [
                ("scaler", StandardScaler()),
                (
                    "gauss",
                    GaussianProcessRegressor(kernel=self.kernel, random_state=0),
                ),
            ]
        )
        return pipe


class SupportVector(Surrogate):
    """
    Class for Support Vector Machine regression.
    """

    def __init__(self, kernel: str = "rbf", degree_fit: int = 2) -> None:
        """

        :param kernel: kernel of SVM
        :type kernel:
        :param degree_fit: Degree of SVM
        :type degree_fit: int

        See https://scikit-learn.org/stable/modules/generated/sklearn.svm.SVR.html
        """
        self.kernel = kernel
        self.degree_fit = degree_fit

    def _model(self) -> Pipeline:
        """
        Method defining the regressor.

        :return: A sklearn pipeline including scaling of predictors.
        :rtype: Pipeline

        """
        pipe = Pipeline(
            [
                ("scaler", StandardScaler()),
                (
                    "svr",
                    SVR(
                        kernel=self.kernel,
                        degree=self.degree_fit,
                    ),
                ),
            ]
        )
        return pipe


class NeuralNetwork(Surrogate):
    """
    Class for Neural Network regression.
    """

    def __init__(
        self,
        n_nodes: Tuple[int, int] = (16, 8),
        activation: str = "relu",
        solver: str = "adam",
        n_epochs: int = 1000,
    ) -> None:
        """

        :param n_nodes: Nodes in each layer
        :type n_nodes: Tuple[int, int]
        :param activation: Activation function of network nodes.
        :type activation: str
        :param solver: Optimized to perform backpropagation.
        :type solver: str
        :param n_epochs: Epochs used for training
        :type n_epochs: int

        See https://scikit-learn.org/stable/modules/generated/sklearn.neural_network.MLPRegressor.html
        """
        self.n_nodes = n_nodes
        self.activation = activation
        self.solver = solver
        self.n_epochs = n_epochs

    def _model(self) -> Pipeline:
        """
        Method defining the regressor.

        :return: A sklearn pipeline including scaling of predictors.
        :rtype: Pipeline
        """
        pipe = Pipeline(
            [
                ("scaler", StandardScaler()),
                (
                    "mlp",
                    MLPRegressor(
                        hidden_layer_sizes=self.n_nodes,
                        activation=self.activation,
                        solver=self.solver,
                        max_iter=self.n_epochs,
                        early_stopping=True,
                    ),
                ),
            ]
        )
        return pipe


class Spline(Surrogate):
    """
    Class for Spline regression.
    """

    def __init__(
        self, n_knots: int = 2, degree_fit: int = 2, fit_intercept: bool = True
    ) -> None:
        """

        :param n_knots: Number of knots to form the spline.
        :type n_knots: int
        :param degree_fit: degree of the fitting polynomials
        :type degree_fit: int
        :param fit_intercept: Whether to fit the intercept
        :type fit_intercept: bool

        See https://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.SplineTransformer.html
        """
        self.n_knots = n_knots
        self.degree_fit = degree_fit
        self.fit_intercept = fit_intercept

    def _model(self) -> Pipeline:
        """
        Method defining the regressor.

        :return: A sklearn pipeline including scaling of predictors.
        :rtype: Pipeline
        """
        pipe = Pipeline(
            [
                ("scaler", StandardScaler()),
                (
                    "spline",
                    SplineTransformer(
                        n_knots=self.n_knots,
                        degree=self.degree_fit,
                    ),
                ),
                (
                    "linear",
                    LinearRegression(fit_intercept=self.fit_intercept),
                ),
            ]
        )
        return pipe
