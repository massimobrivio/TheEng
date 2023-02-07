import operator
from typing import Dict, List, Tuple


def expression_parser(expression: str) -> Tuple[List[str], List[str]]:
    """Parse an expression into a list of operands and a list of operations.

    Args:
        expression (str): The expression to parse.

    Returns:
        Tuple[List[str], List[str]]: A tuple of (operands, operations)
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


def expression_evaluator(
    results: Dict[str, float], operands: List[str], operations: List[str]
) -> float:
    """Evaluate an expression given its operands and operations.

    Args:
        operands (List[str]): List of operands in the expression.
        operations (List[str]): List of operations in the expression.
        results (Dict[str, float]): Dictionary of results from the simulator.

    Raises:
        ValueError: _description_

    Returns:
        float: Result of the expression.
    """

    operands_values = []
    for operand in operands:
        if operand in results:
            operands_values.append(results[operand])
        elif operand == "":
            operands_values.append(0)
        elif test_float(operand):
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


def test_float(x: str) -> bool:
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
