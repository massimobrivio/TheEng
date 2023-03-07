from json import load
from os.path import isfile


class ParseInput:
    def __init__(self):
        self.inputSettings = None

    def parse(self):
        if not self.inputSettings:
            raise ValueError("No input settings found. Run load() first.")
        for k1, v1 in self.inputSettings.items():
            for k2, v2 in v1.items():
                if k2 == "Parameters":
                    for k3, v3 in v2.items():
                        print(k3, v3)
                elif k2 == "Results":
                    for k3, v3 in v2.items():
                        print(k3, v3)
                else:
                    print(k2, v2)

    def load(self, file):
        if not isfile(file):
            raise FileNotFoundError(f"File not found: {file}")
        with open(file, "r") as f:
            self.inputSettings = load(f)


if __name__ == "__main__":
    p = ParseInput()
    p.load("src\\ui\\desktop\\sample.json")
    p.parse()
