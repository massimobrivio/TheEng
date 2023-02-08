# -*- coding: utf-8 -*-

# Macro Begin: C:\Users\brivio\Desktop\Interface.FCMacro +++++++++++++++++++++++++++++++++++++++++++++++++
import json
import sys
from collections import defaultdict
from typing import Dict, List

from abstract import Evaluator
from problem import ProblemConstructor

f = open("configs\\settings.json")
data = json.load(f)
sys.path.append(data["FREECADPATH"])

import FreeCAD
from femtools import ccxtools


class FEModelEvaluator(Evaluator):
    def __init__(
        self,
        problem: ProblemConstructor,
        results_request: List[str],
        path_to_fcd_file: str,
    ) -> None:
        """Initialize an FEM evaluator.

        Args:
            problem (ProblemConstructor): problem to be evaluated.
            results_request (List[str]): list of results aliases contained in the spreadsheet.
            path_to_fcd_file (str): path to the FreeCAD file containing the model.
        """
        super().__init__(problem, results_request, path_to_fcd_file)
        self.doc = FreeCAD.open(self.path_to_fcd_file)
        self.sheet = self.doc.getObject("Spreadsheet")

    def _evaluateSimulator(self, parameters: Dict[str, float]) -> Dict[str, float]:
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
        for result in self.results_request:
            results[result] = self.sheet.get(result)

        return results


class CFDModelEvaluator(Evaluator):
    def __init__(
        self,
        problem: ProblemConstructor,
        results_request: List[str],
        path_to_fcd_file: str,
    ) -> None:
        super().__init__(problem, results_request, path_to_fcd_file)
        raise NotImplementedError("CFDModelEvaluator is not implemented yet.")

    def _evaluateSimulator(self):
        pass
