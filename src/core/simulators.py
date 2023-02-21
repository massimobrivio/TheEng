# -*- coding: utf-8 -*-

# Macro Begin: C:\Users\brivio\Desktop\Interface.FCMacro +++++++++++++++++++++++++++++++++++++++++++++++++
from collections import defaultdict
from json import load
from sys import path
from typing import Dict, List, Iterable

from numpy import max, min, average

f = open("configs\\settings.json")
data = load(f)
path.append(data["FREECAD_PATH"])

import FreeCAD
from femtools import ccxtools


class Simulators:
    def __init__(
        self,
        resultsExpressions: List[str],
        fcdPath: str,
    ) -> None:
        """Initialize an FEM evaluator.

        Args:
            problem (ProblemConstructor): problem to be evaluated.
            resultsRequest (List[str]): list of results aliases contained in the spreadsheet.
            fcdPath (str): path to the FreeCAD file containing the model.
        """
        self.resultsExpressions = resultsExpressions
        self.doc = FreeCAD.open(fcdPath)
        self.sheet = self.doc.getObject("Spreadsheet")

    def femSimulator(self, parameters: Dict[str, float]) -> Dict[str, float]:
        """Evaluate the design parameters and return the results by updating the spreadsheet and running the FEM analysis in FreeCAD.

        Args:
            parameters (Dict[str, float]): dictionary of design parameters containing aliases and values contained in the spreadsheet.

        Returns:
            Dict[str, float]: dictionary containing results aliases and values.
        """

        for key, value in parameters.items():
            self.sheet.set(key, str(value))

        self.sheet.recompute()
        self.doc.recompute()

        fea = ccxtools.FemToolsCcx()
        fea.update_objects()
        fea.setup_working_dir()
        fea.setup_ccx()
        message = fea.check_prerequisites()
        if not message:
            fea.purge_results()
            fea.write_inp_file()
            fea.ccx_run()
            fea.load_results()
        else:
            print(
                "Houston, we have a problem! {}\n".format(message)
            )  # in Python console

        self.sheet.recompute()
        results = defaultdict(float)
        for result in self.resultsExpressions:
            ccx_result = self.sheet.get(result)
            if isinstance(ccx_result, float):
                results[result] = ccx_result
            elif isinstance(ccx_result, Iterable):
                resultMax = result + "Max"
                resultMin = result + "Min"
                resultAvg = result + "Avg"
                results[resultMax] = max(ccx_result)  # type: ignore
                results[resultMin] = min(ccx_result)  # type: ignore
                results[resultAvg] = average(ccx_result)  # type: ignore
            else:
                raise Exception("Result is neither float not Iterable.")

        return results

    def cfdSimulator(self, parameters: Dict[str, float]) -> Dict[str, float]:
        raise NotImplementedError("CFD interface is not implemented yet.")
