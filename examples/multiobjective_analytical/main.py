from problem import ProblemConstructor
from optimizer import NSGA_III

if __name__ == "__main__":
    obj_expression = ["Disp", "Mass"]
    const_expression = ["Mass-1"]

    problem = ProblemConstructor()
    problem.set_objectives(obj_expression)
    problem.set_contraints(const_expression)
    problem.set_bounds({"Length": (200, 500), "Width": (100, 300), "Height": (50, 150)})

    class FunctionEvaluator:
        def __init__(self):
            pass

        def evaluate(self, parameters):
            p = list(parameters.values())
            results = {
                "Disp": (4 * 10000.0 / 193140) * p[0] ** 3 / (p[1] * p[2] ** 3),
                "Mass": p[0] * p[1] * p[2] * 1e-6,
            }
            return results

    evaluator = FunctionEvaluator()
    optimizer = NSGA_III(problem, evaluator, 10)  # type: ignore
    x, f, x_hist, r_hist = optimizer.optimize(("n_eval", 100))

    print(x)
    print(f)
