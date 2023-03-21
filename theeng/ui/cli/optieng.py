import argparse


class CLI:
    def __init__(self) -> None:
        self.parser = argparse.ArgumentParser(
            prog="optieng",
            description="A program for dealing with structural optimization.",
        )
        self._setProblemArguments()

    def run(self):
        args = self.parser.parse_args()
        print(args.parameters)
        print(args.lbs)
        print(args.ubs)
        print(args.targets)
        print(args.operation)

    def _setProblemArguments(self):
        self.parser.add_argument("--parameters", nargs="+", required=False, help="Parameters Names")
        self.parser.add_argument("--lbs", nargs="+", required=False, help="Parameters Lower Bounds")
        self.parser.add_argument("--ubs", nargs="+", required=False, help="Parameters Upper Bounds")

        self.parser.add_argument("--targets", nargs="+", required=False, help="Target Names")
        self.parser.add_argument("--operation", nargs="+", choices=["min", "max", "avg", "none"], required=False, help="Target Names")

    def _setSamplingArguments(self):
        pass

    def _setSurrogateArguments(self):
        pass

    def _setOptimizationArguments(self):
        pass


if __name__ == "__main__":
    cli = CLI()
    cli.run()
