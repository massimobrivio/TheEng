# -*- coding: utf-8 -*-

# Macro Begin: C:\Users\brivio\Desktop\Interface.FCMacro +++++++++++++++++++++++++++++++++++++++++++++++++
from json import load
from sys import path
from collections import defaultdict
from typing import Dict, List

f = open("configs\\settings.json")
data = load(f)
path.append(data["FREECAD_PATH"])

import FreeCAD
from femtools import ccxtools


class Simulators:
    def __init__(
        self,
        resultsRequest: List[str],
        path_to_fcd_file: str,
    ) -> None:
        """Initialize an FEM evaluator.

        Args:
            problem (ProblemConstructor): problem to be evaluated.
            resultsRequest (List[str]): list of results aliases contained in the spreadsheet.
            path_to_fcd_file (str): path to the FreeCAD file containing the model.
        """
        self.resultsRequest = resultsRequest
        self.doc = FreeCAD.open(path_to_fcd_file)
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
        for result in self.resultsRequest:
            results[result] = self.sheet.get(result)

        return results

    def cfdSimulator(self, parameters: Dict[str, float]) -> Dict[str, float]:
        raise NotImplementedError("CFD interface is not implemented yet.")

