from collections import defaultdict
import NXOpen
import NXOpen.CAE
import NXOpen.MenuBar
from typing import List

from theeng.utilities.types import FeatureDefinition


class NXInterface:
    def __init__(
        self,
        features: FeatureDefinition,
        sol_name: str,
        files: dict,
        ncpus: int = 1,
    ) -> None:
        self.parameters = features.pnames
        self.targets = features.tnames
        self.results_measures = []
        self.measurements = []
        for target in features.targets:
            if target.is_objective and not target.is_measurements:
                self.results_measures.append(target.name)
            elif target.is_objective and target.is_measurements:
                self.measurements.append(target.name)
        self.sol_name = sol_name
        self.files = files
        self.ncpus = ncpus

    def objective(self, x: list) -> List[float]:
        result = defaultdict(float)
        x = [str(p) for p in x]
        theSession = NXOpen.Session.GetSession()
        workSimPart = theSession.Parts.BaseWork
        displaySimPart = theSession.Parts.BaseDisplay

        # CAD

        part1 = theSession.Parts.FindObject(self.files["part"])
        status1, partLoadStatus1 = theSession.Parts.SetActiveDisplay(
            part1,
            NXOpen.DisplayPartOption.AllowAdditional,
            NXOpen.PartDisplayPartWorkPartOption.SameAsDisplay,
        )

        workSimPart = NXOpen.BasePart.Null
        workPart = theSession.Parts.Work
        displaySimPart = NXOpen.BasePart.Null
        displayPart = theSession.Parts.Display
        partLoadStatus1.Dispose()

        markId9 = theSession.SetUndoMark(
            NXOpen.Session.MarkVisibility.Invisible, "Make Up to Date"
        )

        objects1 = [NXOpen.NXObject.Null] * len(self.parameters)
        i = 0
        for name, value in zip(self.parameters, x):
            expression_part = workPart.Expressions.FindObject(name)
            workPart.Expressions.EditExpressionWithUnits(
                expression_part, expression_part.Units, value
            )
            objects1[i] = expression_part
            i += 1

        theSession.UpdateManager.MakeUpToDate(objects1, markId9)

        for measurement in self.measurements:
            measure = workPart.Expressions.FindObject(measurement)
            result[measurement] = measure.GetValueUsingUnits(
                measure.UnitsOption.Expression
            )

        # FEM

        femPart1 = theSession.Parts.FindObject(self.files["fem"])
        status2, partLoadStatus2 = theSession.Parts.SetActiveDisplay(
            femPart1,
            NXOpen.DisplayPartOption.AllowAdditional,
            NXOpen.PartDisplayPartWorkPartOption.SameAsDisplay,
        )

        workPart = NXOpen.Part.Null
        workFemPart = theSession.Parts.BaseWork
        displayPart = NXOpen.Part.Null
        displayFemPart = theSession.Parts.BaseDisplay
        partLoadStatus2.Dispose()

        fEModel1 = workFemPart.FindObject("FEModel")
        fEModel1.UpdateFemodel()

        # SIM

        simPart1 = theSession.Parts.FindObject(self.files["sim"])
        status3, partLoadStatus3 = theSession.Parts.SetActiveDisplay(
            simPart1,
            NXOpen.DisplayPartOption.AllowAdditional,
            NXOpen.PartDisplayPartWorkPartOption.SameAsDisplay,
        )

        workSimPart = theSession.Parts.BaseWork
        displaySimPart = theSession.Parts.BaseDisplay
        partLoadStatus3.Dispose()

        theCAESimSolveManager = NXOpen.CAE.SimSolveManager.GetSimSolveManager(
            theSession
        )

        psolutions1 = [NXOpen.CAE.SimSolution.Null] * 1
        simSimulation1 = workSimPart.FindObject("Simulation")
        simSolution1 = simSimulation1.FindObject(f"Solution[{self.sol_name}]")
        propertyTable1 = simSolution1.SolverOptionsPropertyTable
        propertyTable1.SetBooleanPropertyValue("solution monitor", False)
        propertyTable1.SetIntegerPropertyValue("parallel", self.ncpus)

        psolutions1[0] = simSolution1
        (
            numsolutionssolved1,
            numsolutionsfailed1,
            numsolutionsskipped1,
        ) = theCAESimSolveManager.SolveChainOfSolutions(
            psolutions1,
            NXOpen.CAE.SimSolution.SolveOption.Solve,
            NXOpen.CAE.SimSolution.SetupCheckOption.DoNotCheck,
            NXOpen.CAE.SimSolution.SolveMode.Foreground,
        )

        objects3 = [NXOpen.CAE.ResultMeasure.Null] * len(self.results_measures)
        for c, target in enumerate(self.results_measures):
            resultMeasure = simSimulation1.ResultMeasures.Find(
                f"NXOpen.CAE.ResultMeasure[{target}]"
            )
            objects3[c] = resultMeasure
        simSimulation1.ResultMeasures.UpdateMeasures(objects3)

        for object3, result_measure in zip(objects3, self.results_measures):
            result[result_measure] = object3.Result

        final_results = []
        for target_name in self.targets:
            final_results.append(
                result[target_name]
            )  # ordering according to tnames order

        return final_results
