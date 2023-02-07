# -*- coding: utf-8 -*-

# Macro Begin: C:\Users\brivio\Desktop\Interface.FCMacro +++++++++++++++++++++++++++++++++++++++++++++++++
import sys
from collections import defaultdict
from typing import Dict, List

from abstract import Evaluator

FREECADPATH = "C:\\Engineering Programs\\FreeCAD 0.20\\bin"
sys.path.append(FREECADPATH)

import FreeCAD
from femtools import ccxtools


class FEModelEvaluator(Evaluator):
    def __init__(
        self,
        results_request: List[str],
        path_to_fcd_file: str,
    ) -> None:
        """Initialize an FEM evaluator.

        Args:
            results_request (List[str]): list of results aliases contained in the spreadsheet.
            path_to_fcd_file (str): path to the FreeCAD file containing the model.
        """
        super().__init__(results_request, path_to_fcd_file)

    def evaluate(self, parameters: Dict[str, float]) -> Dict[str, float]:
        """Evaluate the design parameters and return the results by updating the spreadsheet and running the FEM analysis in FreeCAD.

        Args:
            parameters (Dict[str, float]): dictionary of design parameters containing aliases and values contained in the spreadsheet.

        Raises:
            Exception: _description_

        Returns:
            Dict[str, float]: dictionary containing results aliases and values.
        """
        doc = FreeCAD.open(self.path_to_fcd_file)
        sheet = doc.getObject("Spreadsheet")

        for key, value in parameters.items():
            sheet.set(key, str(value))

        sheet.recompute()
        doc.recompute()

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

        sheet.recompute()
        results = defaultdict(float)
        for result in self.results_request:
            results[result] = sheet.get(result)

        return results


class CFDModelEvaluator(Evaluator):
    def __init__(
        self,
        parameters: Dict[str, float],
        results_request: List[str],
        path_to_fcd_file: str,
    ) -> None:
        super().__init__(parameters, results_request, path_to_fcd_file)
        raise NotImplementedError("CFDModelEvaluator is not implemented yet.")

    def evaluate(self):
        pass


if __name__ == "__main__":
    parameters = {"Length": 3000.0, "Width": 2200.0, "Height": 1500.0}
    path_to_fcd_file = "C:\\Repositories\\TheEng\\examples\\beam_freecad\\FemCalculixCantilever3D_Param.FCStd"
    results_request = ["Disp"]
    evaluator = FEModelEvaluator(results_request, path_to_fcd_file)
    results = evaluator.evaluate(parameters)
    print(f"Displacement is: {results[results_request[0]]}\n")
