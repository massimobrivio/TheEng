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
                    operands, operations, results
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
                    operands, operations, results
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
            List[Callable[(...), float]]: _description_
        """
        return self._objectives

    def get_constraints(self) -> List[Callable[(...), float]]:
        """Returns a list of callables to evaluate the constraints of the problem.

        Returns:
            List[Callable[(...), float]]: _description_
        """
        return self._constraints

    def get_bounds(self) -> Tuple[List[float], List[float]]:
        """Returns the lower and upper bounds of the problem.

        Returns:
            Tuple[List[float], List[float]]: _description_
        """
        return self._lower_bounds, self._upper_bounds


if __name__ == "__main__":
    bounds = {"x": (5, 10), "y": (6, 12), "z": (0, 3)}
    results = {"A": 2.0, "B": 2, "C": 3}
    obj_expressions = ["A^A + B", "A * B", "A / B", "A / B / C", "A - B - C"]
    constr_expressions = ["A - B", "A + B + C", "A * B * C"]

    problem = ProblemConstructor()
    problem.set_bounds(bounds)
    problem.set_objectives(obj_expressions)
    problem.set_contraints(constr_expressions)

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
