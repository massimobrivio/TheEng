import operator
from typing import Callable, Dict, Iterable, List, Tuple, Union


class ProblemConstructor:
    """The ProblemConstructor class is used to construct the problem to be solved by the optimizer."""

    def __init__(self) -> None:
        """Initialize the ProblemConstructor class."""

        self._objectives = []
        self.objectivesExpressions = []
        self._loweBounds = []
        self._upperBounds = []
        self.boundsExpressions = []
        self._constraints = []
        self.constraintsExpressions = []
        self.resultsExpressions = []
        self.iterableOutput = []

        self.nobj = 0
        self.nconst = 0
        self.nvar = 0
        self.pnames = []

    def setObjectives(self, expressions: List[str]) -> None:
        """Set the objectives of the problem.

        Args:
            expressions (List[str]): List of expressions encoded as strings.
        """

        ProblemConstructor._checkExpressions(expressions)

        for expression in expressions:
            operands, operations = ProblemConstructor._expressionParser(expression)
            self._objectives.append(
                lambda results, operands=operands, operations=operations: ProblemConstructor._expressionEvaluator(
                    results, operands, operations
                )
            )
            self.nobj += 1
        self.objectivesExpressions = expressions

    def setContraints(self, expressions: List[str]) -> None:
        """Set the constraints of the problem.

        Args:
            expressions (List[str]): List of expressions encoded as strings. They will be considered <= 0.
        """

        ProblemConstructor._checkExpressions(expressions)

        for expression in expressions:
            operands, operations = ProblemConstructor._expressionParser(expression)
            self._constraints.append(
                lambda results, operands=operands, operations=operations: ProblemConstructor._expressionEvaluator(
                    results, operands, operations
                )
            )
            self.nconst += 1
        self.constraintsExpressions = expressions

    def setBounds(self, bounds: Dict[str, Tuple[float, float]]) -> None:
        """Set the bounds of the problem.

        Args:
            bounds (Dict[str, Tuple[float, float]]): A dictionary of the form {parameter: (lower_bound, upper_bound)}
        """

        ProblemConstructor._checkBounds(bounds)

        for key, value in bounds.items():
            self._loweBounds.append(value[0])
            self._upperBounds.append(value[1])
            self.boundsExpressions.append(f"{value[0]} <= {key} <= {value[1]}")
            self.nvar += 1
            self.pnames.append(key)

    def setResults(self, expressions: Dict[str, Union[None, str]]) -> None:
        """Set the results to get from the simulation.

        Args:
            expressions (List[str]): List of results name as set in the FreeCAD spreadsheet.
        """
        expressionNames = list(expressions.keys())
        ProblemConstructor._checkExpressions(expressionNames)

        self.resultsExpressions = expressionNames
        self.iterableOutput = list(expressions.values())

    def getObjectives(self) -> List[Callable[(...), float]]:
        """Returns a list of callables to evaluate the objectives of the problem.

        Returns:
            List[Callable[(...), float]]: List of callables to evaluate the objectives of the problem.
        """
        return self._objectives

    def getConstraints(self) -> List[Callable[(...), float]]:
        """Returns a list of callables to evaluate the constraints of the problem.

        Returns:
            List[Callable[(...), float]]: List of callables to evaluate the constraints of the problem.
        """
        return self._constraints

    def getBounds(self) -> Tuple[List[float], List[float]]:
        """Returns the lower and upper bounds of the problem.

        Returns:
            Tuple[List[float], List[float]]: List of lower bounds and list of upper bounds.
        """
        return self._loweBounds, self._upperBounds

    def getResultsExpressions(self) -> List[str]:
        """Returns the names of the results from the simulation.

        Returns:
            List[str]: List of names of results.
        """
        return self.resultsExpressions

    def getIterableOutput(self) -> List[Union[None, str]]:
        """Specify how to treat iterable results from the simulation.

        Returns:
            List[str]: List of actions to perform on iterable results.
        """
        return self.iterableOutput

    def getPnames(self) -> List[str]:
        """Returns the names of the parameters.

        Returns:
            List[str]: The parameters names.
        """
        return self.pnames

    def getNobj(self) -> int:
        """Returns the number of objectives.

        Returns:
            int: The number of objectives.
        """
        return self.nobj

    def getNconst(self) -> int:
        """Returns the number of constraints.

        Returns:
            int: The number of constraints.
        """
        return self.nconst

    def getNvar(self) -> int:
        """Returns the number of variables.

        Returns:
            int: The number of variables.
        """
        return self.nvar

    def getObjectivesExpressions(self) -> List[str]:
        """Returns the list of objectives expressions.

        Returns:
            List[str]: A list of objectives expressions.
        """
        return self.objectivesExpressions

    def getConstraintsExpressions(self) -> List[str]:
        """Returns the list of constraints expressions.

        Returns:
            List[str]: A list of constraints expressions.
        """
        return self.constraintsExpressions

    @staticmethod
    def _expressionParser(expression: str) -> Tuple[List[str], List[str]]:
        """Parse an expression into a list of operands and a list of operations.

        Args:
            expression (str): The expression to parse.

        Returns:
            Tuple[List[str], List[str]]: A tuple of (operands, operations)

        Merit:
            This function is based on the following merit:
            Stack Overflow: https://stackoverflow.com/questions/13055884/parsing-math-expression-in-python-and-solving-to-find-an-answer
            Author: https://stackoverflow.com/users/748858/mgilson
        """
        expression = expression.replace(" ", "")
        operators = set("^+-*/")
        operations = (
            []
        )  # This holds the operators that are found in the string (left to right)
        operands = (
            []
        )  # this holds the non-operators that are found in the string (left to right)
        buff = []
        for c in expression:  # examine 1 character at a time
            if c in operators:
                # found an operator.  Everything we've accumulated in `buff` is
                # a single "number". Join it together and put it in `operands`.
                operands.append("".join(buff))
                buff = []
                operations.append(c)
            else:
                # not an operator.  Just accumulate this character in buff.
                buff.append(c)
        operands.append("".join(buff))
        return operands, operations

    @staticmethod
    def _expressionEvaluator(
        results: Dict[str, float], operands: List[str], operations: List[str]
    ) -> float:
        """Evaluate an expression given its operands and operations.

        Args:
            operands (List[str]): List of operands in the expression.
            operations (List[str]): List of operations in the expression.
            results (Dict[str, float]): Dictionary of results from the simulator.

        Raises:
            ValueError: When a operand used in the expression is not known.

        Returns:
            float: Result of the expression.

        Merit:
            This function is based on the following merit:
            Stack Overflow: https://stackoverflow.com/questions/13055884/parsing-math-expression-in-python-and-solving-to-find-an-answer
            Author: https://stackoverflow.com/users/748858/mgilson
        """

        operands_values = []
        for operand in operands:
            if operand in results:
                operands_values.append(results[operand])
            elif operand == "":
                operands_values.append(0)
            elif ProblemConstructor._testFloat(operand):
                operands_values.append(float(operand))
            else:
                raise ValueError(f"Unknown operand {operand}")

        operator_order = (
            "^",
            "*/",
            "+-",
        )  # precedence from left to right.  operators at same index have same precendece.
        # map operators to functions.
        op_dict = {
            "*": operator.mul,
            "/": operator.truediv,
            "+": operator.add,
            "-": operator.sub,
            "^": operator.pow,
        }

        operations_copy = operations.copy()

        for op in operator_order:  # Loop over precedence levels
            while any(
                o in operations_copy for o in op
            ):  # Operator with this precedence level exists
                idx, oo = next(
                    (i, o) for i, o in enumerate(operations_copy) if o in op
                )  # Next operator with this precedence
                operations_copy.pop(idx)  # remove this operator from the operator list
                values = map(
                    float, operands_values[idx : idx + 2]
                )  # here I just assume float for everything
                value = op_dict[oo](*values)
                operands_values[idx : idx + 2] = [value]  # clear out those indices

        return operands_values[0]

    @staticmethod
    def _checkExpressions(expressions: List[str]) -> bool:
        """_summary_

        Args:
            expression (List[str]): Expressions to be checked.

        Raises:
            TypeError: If any expressions are not encoded as strings.

        Returns:
            bool: True if all expressions are encoded as strings.
        """
        if all([isinstance(exp, str) for exp in expressions]):
            return True
        else:
            raise TypeError("The expressions must be encoded as strings.")

    @staticmethod
    def _checkBounds(bounds: Dict[str, Tuple[float, float]]) -> bool:  # type: ignore
        """_summary_

        Args:
            bounds (Dict[str, Tuple[float, float]]): Bounds to be checked.

        Raises:
            TypeError: If the bounds are not encoded as a dictionary.

        Returns:
            bool: True if the bounds are encoded as a dictionary.
        """
        if isinstance(bounds, dict):
            for name, value in bounds.items():
                name_check = isinstance(name, str)
                value_check = isinstance(value, Iterable)
                number_check = all([isinstance(num, (int, float)) for num in value])
                dim_check = value[0] < value[1]

                if not dim_check:
                    raise ValueError(
                        "The upper bound must be greater than the lower bound."
                    )
                elif not number_check:
                    raise TypeError("The bounds values must be integers or floats.")
                elif not value_check:
                    raise TypeError("The bounds values must be encoded as tuples.")
                elif not name_check:
                    raise TypeError("The bounds keys must be strings.")
                else:
                    return True
        else:
            raise TypeError("The bounds must be encoded as a dictionary.")

    @staticmethod
    def _testFloat(x: str) -> bool:
        """Test if a string can be converted to a float.

        Args:
            x (str): String to be tested.

        Returns:
            bool: True if the string can be converted to a float, False otherwise.
        """
        try:
            float(x)
            return True
        except ValueError:
            return False


if __name__ == "__main__":
    bounds = {"x": (5, 10), "y": (6, 12), "z": (0, 3)}
    results = {"Disp": 0.5, "B": 2.0, "C": 3}
    obj_expressions = [
        "Disp^2",
        "-Disp * B",
        "Disp / B",
        "Disp / B / C",
        "Disp - B - C",
    ]
    constr_expressions = ["Disp - 2", "Disp + B + C", "Disp * B * C"]

    problem = ProblemConstructor()
    problem.setObjectives(obj_expressions)
    problem.setContraints(constr_expressions)
    problem.setBounds(bounds)

    for i, obj in enumerate(problem.getObjectives()):
        print(f"Objective Value nr. {i}: {obj(results)}")
        print(f"Objective Expression nr. {i}: {problem.objectivesExpressions[i]}")
    print("\n\n")
    for i, constr in enumerate(problem.getConstraints()):
        print(f"Constraint nr. {i}: {constr(results)}")
        print(f"Constraint Expression nr. {i}: {problem.constraintsExpressions[i]}")
    print("\n\n")
    i = 0
    for lb, ub in zip(*problem.getBounds()):
        print(f"Bound nr. {i}: {lb} - {ub}")
        print(f"Bound Expression nr. {i}: {problem.boundsExpressions[i]}")
        i += 1
