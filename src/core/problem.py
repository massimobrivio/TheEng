from typing import Callable, Dict, List, Tuple
from utilities import expression_parser, expression_evaluator


class ProblemConstructor:
    """The ProblemConstructor class is used to construct the problem to be solved by the optimizer."""

    def __init__(self) -> None:
        """Initialize the ProblemConstructor class."""

        self._objectives = []
        self.objectives_expressions = []
        self._lower_bounds = []
        self._upper_bounds = []
        self.bounds_expressions = []
        self._constraints = []
        self.constraints_expressions = []

        self.nobj = 0
        self.nconst = 0
        self.nvar = 0
        self.pnames = []

    def set_objectives(self, expressions: List[str]) -> None:
        """Set the objectives of the problem.

        Args:
            expressions (List[str]): List of expressions encoded as strings.
        """
        for expression in expressions:
            operands, operations = expression_parser(expression)
            self._objectives.append(
                lambda results, operands=operands, operations=operations: expression_evaluator(
                    results, operands, operations
                )
            )
            self.nobj += 1
        self.objectives_expressions = expressions

    def set_contraints(self, expressions: List[str]) -> None:
        """Set the constraints of the problem.

        Args:
            expressions (List[str]): List of expressions encoded as strings. They will be considered <= 0.
        """
        for expression in expressions:
            operands, operations = expression_parser(expression)
            self._constraints.append(
                lambda results, operands=operands, operations=operations: expression_evaluator(
                    results, operands, operations
                )
            )
            self.nconst += 1
        self.constraints_expressions = expressions

    def set_bounds(self, bounds: Dict[str, Tuple[float, float]]) -> None:
        """Set the bounds of the problem.

        Args:
            bounds (Dict[str, Tuple[float, float]]): A dictionary of the form {parameter: (lower_bound, upper_bound)}
        """
        for key, value in bounds.items():
            self._lower_bounds.append(value[0])
            self._upper_bounds.append(value[1])
            self.bounds_expressions.append(f"{value[0]} <= {key} <= {value[1]}")
            self.nvar += 1
            self.pnames.append(key)

    def get_objectives(self) -> List[Callable[(...), float]]:
        """Returns a list of callables to evaluate the objectives of the problem.

        Returns:
            List[Callable[(...), float]]: List of callables to evaluate the objectives of the problem.
        """
        return self._objectives

    def get_constraints(self) -> List[Callable[(...), float]]:
        """Returns a list of callables to evaluate the constraints of the problem.

        Returns:
            List[Callable[(...), float]]: List of callables to evaluate the constraints of the problem.
        """
        return self._constraints

    def get_bounds(self) -> Tuple[List[float], List[float]]:
        """Returns the lower and upper bounds of the problem.

        Returns:
            Tuple[List[float], List[float]]: List of lower bounds and list of upper bounds.
        """
        return self._lower_bounds, self._upper_bounds

    def get_pnames(self) -> List[str]:
        """Returns the names of the parameters.

        Returns:
            List[str]: The parameters names.
        """
        return self.pnames

    def get_nobj(self) -> int:
        """Returns the number of objectives.

        Returns:
            int: The number of objectives.
        """
        return self.nobj

    def get_nconst(self) -> int:
        """Returns the number of constraints.

        Returns:
            int: The number of constraints.
        """
        return self.nconst

    def get_nvar(self) -> int:
        """Returns the number of variables.

        Returns:
            int: The number of variables.
        """
        return self.nvar

    def get_objectives_expressions(self) -> List[str]:
        """Returns the list of objectives expressions.

        Returns:
            List[str]: A list of objectives expressions.
        """
        return self.objectives_expressions

    def get_constraints_expressions(self) -> List[str]:
        """Returns the list of constraints expressions.

        Returns:
            List[str]: A list of constraints expressions.
        """
        return self.constraints_expressions


if __name__ == "__main__":
    bounds = {"x": (5, 10), "y": (6, 12), "z": (0, 3)}
    results = {"Disp": 0.5, "B": 2.0, "C": 3}
    obj_expressions = ["Disp^2", "Disp * B", "Disp / B", "Disp / B / C", "Disp - B - C"]
    constr_expressions = ["Disp - 2", "Disp + B + C", "Disp * B * C"]

    problem = ProblemConstructor()
    problem.set_objectives(obj_expressions)
    problem.set_contraints(constr_expressions)
    problem.set_bounds(bounds)

    for i, obj in enumerate(problem.get_objectives()):
        print(f"Objective Value nr. {i}: {obj(results)}")
        print(f"Objective Expression nr. {i}: {problem.objectives_expressions[i]}")
    print("\n\n")
    for i, constr in enumerate(problem.get_constraints()):
        print(f"Constraint nr. {i}: {constr(results)}")
        print(f"Constraint Expression nr. {i}: {problem.constraints_expressions[i]}")
    print("\n\n")
    i = 0
    for lb, ub in zip(*problem.get_bounds()):
        print(f"Bound nr. {i}: {lb} - {ub}")
        print(f"Bound Expression nr. {i}: {problem.bounds_expressions[i]}")
        i += 1
