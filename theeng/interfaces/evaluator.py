# -*- coding: utf-8 -*-

# Macro Begin: C:\Users\brivio\Desktop\Interface.FCMacro +++++++++++++++++++++++++++++++++++++++++++++++++
import FreeCAD
import FreeCADGui
import FemGui
from femtools import ccxtools
from typing import Dict, List
from collections import defaultdict


def evaluate(parameters: Dict[str, float], results_request: List[str]) -> Dict[str, float]:
    """
    Evaluate the design parameters and return the results by updating the spreadsheet and running the FEM analysis in FreeCAD.

    Args:
        parameters (Dict[str, float]): dictionary of design parameters containing aliases and values contained in the spreadsheet.
        results_request (List[str]): list of results aliases contained in the spreadsheet.

    Raises:
        Exception: _description_

    Returns:
        _type_: _description_
    """
    doc = App.ActiveDocument
    sheet = doc.getObject("Spreadsheet")

    for key, value in parameters.items():
        sheet.set(key, str(value))

    sheet.recompute()

    FreeCADGui.ActiveDocument.activeView().viewAxonometric()
    FreeCADGui.SendMsgToActiveView("ViewFit")

    doc.recompute()

    FemGui.setActiveAnalysis(doc.Analysis)

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
        FreeCAD.Console.PrintError(
            "Houston, we have a problem! {}\n".format(message)
        )  # in report view
        print("Houston, we have a problem! {}\n".format(message))  # in Python console
        
    sheet.recompute()
    results = defaultdict(float)
    for result in results_request:
        results[result] = sheet.get(result)
    
    return results
    

if __name__ == "__main__":
    parameters = {"Length": 4000, "Width": 2200, "Height": 1500}
    results_request = ["Disp"]
    results = evaluate(parameters, results_request)
    FreeCAD.Console.PrintMessage(
            f"Displacement is: {results[results_request[0]]}\n"
        )
