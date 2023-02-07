from os.path import join, isfile

# from email.mime.multipart import MIMEMultipart
# from email.mime.text import MIMEText
from typing import Callable, Tuple, List, Dict, Union
from joblib import dump, load

from pandas import DataFrame

from src.blocks.data import Data
from src.blocks.optimization import (
    NSGA_III,
    ParticleSwarm,
    GeneticAlgorithm,
    NelderMeadSearch,
)
from src.blocks.postprocessing import Decision
from src.blocks.sampling import Latin, Random
from src.blocks.surrogates import (
    Kriging,
    NeuralNetwork,
    Polynomial,
    Spline,
    SupportVector,
)
from pymoo.operators.sampling.rnd import FloatRandomSampling
from pymoo.core.population import Population
from src.utilities.types import FeatureDefinition


class AiDev:
    def __init__(
        self,
        features: FeatureDefinition,
        simulator: Callable[..., List[float]],
        path: str,
    ):
        """_summary_

        Args:
            features (FeatureDefinition): _description_
            simulator (Callable[..., List[float]]): _description_
            path (str): _description_
        """
        self.features = features
        self.simulator = simulator
        self.path = path

        self.data = DataFrame()
        self.datahandler = Data(
            features=self.features,
            simulator=self.simulator,
        )

        self.sampling_strategy = "latin"
        self.n_samples = 50

        self.optimization_strategy = "global"
        self.global_optimizer = "PSO"
        self.popsize = 15
        self.local_iter = 500
        self.global_iter = 5

        self.surrogate_strategy = "polynomial"
        self.degree_fit = 1
        self.interaction_only = False
        self.fit_intercept = True
        self.kernel = "rbf"
        self.n_nodes = (16, 8)
        self.activation = "relu"
        self.n_epochs = 1000
        self.n_knots = 2

    def run(
        self,
        data: DataFrame = DataFrame(),
        sampling: bool = True,
        surrogate: bool = True,
        optimization: bool = True,
        restart: bool = False
        # mail_at_completion=False
    ) -> DataFrame:
        """_summary_

        Args:
            data (DataFrame, optional): _description_. Defaults to DataFrame().
            sampling (bool, optional): _description_. Defaults to True.
            surrogate (bool, optional): _description_. Defaults to True.
            optimization (bool, optional): _description_. Defaults to True.
            restart (bool, optional): _description_. Defaults to False.

        Returns:
            DataFrame: _description_
        """
        if not data.empty:
            self.data = data.dropna().drop_duplicates()[
                self.features.pnames + self.features.tnames
            ]

        if sampling:
            doe = self._sampling()
            if not self.data.empty:
                self.data = self.datahandler.add(data=self.data, samples=doe)
            else:
                self.data = self.datahandler.generate(samples=doe)

            # self.data = self._decision()
            self.data.to_csv(join(self.path, "db.csv"), index=False, mode="w")

        if optimization:

            if restart:
                if isfile(join(self.path, "restart.pkl")):
                    restart_pop = load(join(self.path, "restart.pkl"))
                else:
                    raise FileNotFoundError("Restart file not found in working directory, please indicate one or select restart=False.")
            else:
                restart_pop = FloatRandomSampling()

            if surrogate:
                for _ in range(self.global_iter):
                    simulator_surrogate, _ = self._surrogate()
                    results = self._optimization(simulator_surrogate, surrogate=True, restart_pop=restart_pop)
                    x_results = results["x"]
                    self.data = self.datahandler.add(data=self.data, samples=x_results)  # type: ignore
            else:
                results = self._optimization(self.simulator, surrogate=False, restart_pop=restart_pop)
                x_hist = results["x_hist"]
                fval_hist = results["fval_hist"]

                if not self.data.empty:
                    self.data = self.datahandler.add(
                        data=self.data, samples=x_hist, fval=fval_hist
                    )
                else:
                    self.data = self.datahandler.generate(
                        samples=x_hist, fval=fval_hist
                    )

            last_pop = results["last_pop"]
            self.data = self._decision()

            dump(last_pop, join(self.path, "restart.pkl"))
            self.data.to_csv(join(self.path, "db.csv"), index=False, mode="w")

        return self.data

    def _sampling(self) -> DataFrame:
        """_summary_

        Returns:
            DataFrame: _description_
        """
        if self.sampling_strategy == "latin":
            doe = Latin(self.features)(n_samples=self.n_samples)
        else:
            doe = Random(self.features)(n_samples=self.n_samples)
        return doe

    def _surrogate(
        self,
    ) -> Tuple[Callable[..., List[float]], Tuple[float, float]]:
        """_summary_

        Returns:
            Tuple[Callable[..., List[float]], Tuple[float, float]]: _description_
        """

        if self.surrogate_strategy == "kriging":
            model, performance = Kriging(kernel=None)(self.data, self.features)
        elif self.surrogate_strategy == "supportvector":
            model, performance = SupportVector(
                kernel=self.kernel,
                degree_fit=self.degree_fit,
            )(self.data, self.features)
        elif self.surrogate_strategy == "neuralnetwork":
            model, performance = NeuralNetwork(
                n_nodes=self.n_nodes,
                activation=self.activation,
                n_epochs=self.n_epochs,
            )(self.data, self.features)
        elif self.surrogate_strategy == "spline":
            model, performance = Spline(
                n_knots=self.n_knots,
                degree_fit=self.degree_fit,
                fit_intercept=self.fit_intercept,
            )(self.data, self.features)
        else:
            model, performance = Polynomial(
                degree_fit=self.degree_fit,
                interaction_only=self.interaction_only,
                fit_intercept=self.fit_intercept,
            )(self.data, self.features)

        return model, performance

    def _optimization(
        self,
        objective: Callable[..., List[float]],
        surrogate: bool = False,
        restart_pop: Union[FloatRandomSampling, Population] = FloatRandomSampling()
    ) -> Dict[str, DataFrame]:
        """_summary_

        Args:
            objective (Callable[..., List[float]]): _description_
            surrogate (bool, optional): _description_. Defaults to True.

        Returns:
            Dict[str, DataFrame]: _description_
        """
        if self.features.nobjs == 1:
            termination = (
                ("n_gen", self.local_iter)
                if surrogate
                else ("n_eval", self.global_iter)
            )
            if self.optimization_strategy == "local":
                results = NelderMeadSearch(
                    objective,
                    self.features,
                    popsize=self.popsize,
                )(termination=termination)
            else:
                if self.global_optimizer == "GA":
                    results = GeneticAlgorithm(
                        objective,
                        self.features,
                        popsize=self.popsize,
                        restart_pop=restart_pop
                    )(termination=termination)
                else:
                    results = ParticleSwarm(
                        objective,
                        self.features,
                        popsize=self.popsize,
                        restart_pop=restart_pop
                    )(termination=termination)
        else:
            termination = (
                ("n_gen", self.local_iter)
                if surrogate
                else ("n_eval", self.global_iter)
            )
            results = NSGA_III(objective, self.features, popsize=self.popsize,
                               restart_pop=restart_pop)(
                termination=termination
            )
        return results

    def _decision(self, return_choices: int = 10) -> DataFrame:
        """_summary_

        Args:
            return_choices (int, optional): _description_. Defaults to 10.

        Returns:
            DataFrame: _description_
        """
        data = Decision(self.features).decide(
            self.data, return_choices=return_choices  # type: ignore
        )
        return data

    # @staticmethod
    # def _mail(content: str):
    #     with open("../../settings.json") as settings_file:
    #         settings = load(settings_file)
    #     message = MIMEMultipart()
    #     sender_address = settings["sender_address"]
    #     sender_psw = settings["sender_psw"]
    #     receiver_address = settings["receiver_address"]
    #
    #     message["From"] = sender_address
    #     message["To"] = receiver_address
    #     message["Subject"] = "Notification of AiDev process end."
    #     message.attach(MIMEText(content, "plain"))
    #
    #     session = smtplib.SMTP("smtp.gmail.com", 587)
    #     session.starttls()
    #     session.login(sender_address, sender_psw)
    #     text = message.as_string()
    #     session.sendmail(sender_address, receiver_address, text)
    #     session.quit()
