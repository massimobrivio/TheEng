import sys
from abc import abstractmethod
from json import dump
from os import environ
from os.path import join
from typing import Dict, List

from PyQt5.QtWidgets import (
    QApplication,
    QCheckBox,
    QComboBox,
    QDialog,
    QDoubleSpinBox,
    QGridLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QSizePolicy,
    QSpacerItem,
    QSpinBox,
    QTabWidget,
    QVBoxLayout,
    QWidget,
)

from theeng.theeng import TheEng


class Group(QGroupBox):
    def __init__(self, title: str, labels: List[str], isDynamic: bool = False):
        super().__init__()

        mainLayout = QVBoxLayout()

        self.settingsWidgets = self.setWidgetList()
        self.settingsLabels = [QLabel(label) for label in labels]

        assert len(self.settingsLabels) == len(self.settingsWidgets), Exception(
            "Length of given labels should be the same as the len of given widgets"
        )

        self.groupList = [self.settingsLabels, self.settingsWidgets]

        self.settingsLayout = QGridLayout()
        for rowNumber, groupRow in enumerate(self.groupList):
            for columnNumber, widget in enumerate(groupRow):
                self.settingsLayout.addWidget(widget, rowNumber, columnNumber)

        mainLayout.addLayout(self.settingsLayout)

        if isDynamic:
            self.addClicked = 1
            self.addButton = QPushButton("Add")
            self.addButton.clicked.connect(self.addRow)
            self.removeButton = QPushButton("Remove")
            self.removeButton.clicked.connect(self.removeRow)
            addremoveLayout = QHBoxLayout()
            addremoveLayout.addWidget(self.addButton)
            addremoveLayout.addWidget(self.removeButton)
            mainLayout.addLayout(addremoveLayout)

        self.setTitle(title)
        self.setLayout(mainLayout)

    @abstractmethod
    def setWidgetList(self) -> List[QWidget]:  # type: ignore
        pass

    @abstractmethod
    def getSettings(self) -> Dict:  # type: ignore
        pass

    def addRow(self):
        newSettingsWidgets = self.setWidgetList()
        self.groupList.append(newSettingsWidgets)
        for widgetCount, widget in enumerate(newSettingsWidgets):
            self.settingsLayout.addWidget(widget, len(self.groupList) + 1, widgetCount)
        self.addClicked += 1

    def removeRow(self):
        for widget in self.groupList[-1]:
            self.settingsLayout.removeWidget(widget)
        self.groupList.pop()
        self.addClicked -= 1


class SideBar(QGroupBox):
    def __init__(self):
        super().__init__()
        self.workingDirectoryLabel = QLabel("Working Directory")
        self.workingDirectoryLine = QLineEdit()
        self.workingDirectoryLine.setPlaceholderText("Enter working directory...")
        self.workingDirectoryLine.setText(join(join(environ["USERPROFILE"]), "Desktop"))

        self.simulationDirectoryLabel = QLabel("Simulation Directory")
        self.simulationDirectoryLine = QLineEdit()
        self.simulationDirectoryLine.setPlaceholderText("Enter simulation directory...")

        self.simulatorNameLabel = QLabel("Simulation Name")
        self.simulatorNameLine = QComboBox()
        self.simulatorNameLine.addItems(["femSimulator", "cfdSimulator"])

        self.nCpusLabel = QLabel("Number of CPUs")
        self.nCpusSpinBox = QSpinBox()
        self.nCpusSpinBox.setValue(2)

        self.surrogateLabel = QLabel("Enable Surrogate")
        self.surrogateCheckBox = QCheckBox()
        self.surrogateCheckBox.setChecked(True)

        verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)  # type: ignore

        sidebarLayout = QVBoxLayout()
        sidebarLayout.addWidget(self.workingDirectoryLabel)
        sidebarLayout.addWidget(self.workingDirectoryLine)
        sidebarLayout.addWidget(self.simulationDirectoryLabel)
        sidebarLayout.addWidget(self.simulationDirectoryLine)
        sidebarLayout.addWidget(self.simulatorNameLabel)
        sidebarLayout.addWidget(self.simulatorNameLine)
        sidebarLayout.addWidget(self.nCpusLabel)
        sidebarLayout.addWidget(self.nCpusSpinBox)
        sidebarLayout.addWidget(self.surrogateLabel)
        sidebarLayout.addWidget(self.surrogateCheckBox)
        sidebarLayout.addSpacerItem(verticalSpacer)

        self.setTitle("Global Settings")
        self.setLayout(sidebarLayout)

    def getSideBarSettings(self):
        settings = {
            "Working Directory": self.workingDirectoryLine.text(),
            "Simulation Directory": self.simulationDirectoryLine.text(),
            "Simulator Name": self.simulatorNameLine.currentText(),
            "Use Surrogate": self.surrogateCheckBox.isChecked(),
            "nCPUs": self.nCpusSpinBox.value(),
        }
        return settings

    def getWorkingDirectory(self):
        return self.workingDirectoryLine.text()


class ParametersDefinition(Group):
    def __init__(
        self,
        title="Parameter Settings",
        labels=["Parameter Name", "Lower Bounds", "Upper Bounds"],
        isDynamic: bool = True,
    ):
        super().__init__(title, labels, isDynamic)

    def setWidgetList(self) -> List[QWidget]:
        parameterNameLine = QLineEdit()
        parameterNameLine.setPlaceholderText("Enter parameter name...")
        lowerBoundDoubleSpinBox = QDoubleSpinBox()
        lowerBoundDoubleSpinBox.setValue(0.0)
        lowerBoundDoubleSpinBox.setRange(-1e20, 1e20)
        upperBoundDoubleSpinBox = QDoubleSpinBox()
        upperBoundDoubleSpinBox.setValue(0.0)
        upperBoundDoubleSpinBox.setRange(-1e20, 1e20)
        return [parameterNameLine, lowerBoundDoubleSpinBox, upperBoundDoubleSpinBox]

    def getSettings(self) -> Dict:
        results = {}
        for (
            parameterNameLine,
            lowerBoundDoubleSpinBox,
            upperBoundDoubleSpinBox,
        ) in self.groupList[1:]:
            results[parameterNameLine.text()] = (
                lowerBoundDoubleSpinBox.value(),
                upperBoundDoubleSpinBox.value(),
            )
        return results


class ResultsDefinition(Group):
    def __init__(
        self,
        title="Results Settings",
        labels=["Result Name", "Result Operation"],
        isDynamic=True,
    ):
        super().__init__(title, labels, isDynamic)

    def setWidgetList(self) -> List[QWidget]:
        resultNameLine = QLineEdit()
        resultNameLine.setPlaceholderText("Enter Result name...")
        resultOperationComboBox = QComboBox()
        resultOperationComboBox.addItems(["None", "Max", "Min", "Avg"])
        return [resultNameLine, resultOperationComboBox]

    def getSettings(self) -> Dict:
        results = {}
        for (
            resultNameLine,
            resultOperationComboBox,
        ) in self.groupList[1:]:
            results[resultNameLine.text()] = resultOperationComboBox.currentText()
        return results


class ObjectiveDefinition(Group):
    def __init__(
        self,
        title="Objective Settings",
        labels=["Objective Expression", "Objective Weight"],
        isDynamic=True,
    ):
        super().__init__(title, labels, isDynamic)

    def setWidgetList(self) -> List[QWidget]:
        objectiveNameLine = QLineEdit()
        objectiveNameLine.setPlaceholderText("Enter Objective Expression...")
        objectiveWeightSpinBox = QDoubleSpinBox()
        objectiveWeightSpinBox.setValue(0.5)
        objectiveWeightSpinBox.setSingleStep(0.1)
        objectiveWeightSpinBox.setRange(0.0, 1.0)
        return [objectiveNameLine, objectiveWeightSpinBox]

    def getSettings(self) -> Dict:
        results = {}
        for (
            objectiveNameLine,
            objectiveWeightSpinBox,
        ) in self.groupList[1:]:
            results[objectiveNameLine.text()] = objectiveWeightSpinBox.value()
        return results


class ConstraintDefinition(Group):
    def __init__(
        self,
        title="Constraints Settings",
        labels=["Constraint Expression", "Constraint Relaxation"],
        isDynamic=True,
    ):
        super().__init__(title, labels, isDynamic)

    def setWidgetList(self) -> List[QWidget]:
        constraintNameLine = QLineEdit()
        constraintNameLine.setPlaceholderText("Enter Constraints Expression...")
        constraintRelaxationSpinBox = QDoubleSpinBox()
        constraintRelaxationSpinBox.setValue(10.0)
        constraintRelaxationSpinBox.setRange(0.0, 100)
        return [constraintNameLine, constraintRelaxationSpinBox]

    def getSettings(self) -> Dict:
        results = {}
        for (
            constraintNameLine,
            constraintRelaxationSpinBox,
        ) in self.groupList[1:]:
            results[constraintNameLine.text()] = constraintRelaxationSpinBox.value()
        return results


# class SamplingDefinition(Group):
#     def __init__(
#         self,
#         title="Sampling Settings",
#         labels=[
#             "Sampling Method",
#             "Number of Samples"
#         ],
#         isDynamic=False,
#     ):
#         super().__init__(title, labels, isDynamic)

#     def setWidgetList(self) -> List[QWidget]:
#         methodComboBox = QComboBox()
#         methodComboBox.addItems(["latinHypercube", "random"])
#         nSamplesSpinBox = QSpinBox()
#         nSamplesSpinBox.setValue(50)
#         nSamplesSpinBox.setRange(1, 10000)
#         return [methodComboBox, nSamplesSpinBox]

#     def getSettings(self) -> Dict:
#         results = {}
#         for methodComboBox, nSamplesSpinBox in self.groupList[1:]:
#             results[methodComboBox.currentText()] = nSamplesSpinBox.value()
#         return results

#     def addRow(self):
#         pass

#     def removeRow(self):
#         pass


# class SamplingTab(QWidget):
#     def __init__(self):
#         super().__init__()
#         self.samplingDefinition = SamplingDefinition()
#         verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)  # type: ignore

#         mainLayout = QVBoxLayout()
#         mainLayout.addWidget(self.samplingDefinition)
#         mainLayout.addSpacerItem(verticalSpacer)

#         self.setLayout(mainLayout)

#     def getSettings(self):
#         return self.samplingDefinition.getSettings()


class ProblemTab(QWidget):
    def __init__(self):
        super().__init__()
        self.parametersDefinition = ParametersDefinition()
        self.resultsDefinition = ResultsDefinition()
        verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)  # type: ignore

        mainLayout = QVBoxLayout()
        mainLayout.addWidget(self.parametersDefinition)
        mainLayout.addWidget(self.resultsDefinition)
        mainLayout.addSpacerItem(verticalSpacer)

        self.setLayout(mainLayout)

    def getProblemSettings(self):
        parameterSettings = self.parametersDefinition.getSettings()
        resultSettings = self.resultsDefinition.getSettings()
        return {"Parameters": parameterSettings, "Results": resultSettings}


class SamplingTab(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.methodLabel = QLabel("Sampling Method")
        self.methodComboBox = QComboBox()
        self.methodComboBox.addItems(["latinHypercube", "random"])
        self.nSamplesLabel = QLabel("Number of Samples")
        self.nSamplesSpinBox = QSpinBox()
        self.nSamplesSpinBox.setValue(50)
        self.nSamplesSpinBox.setRange(1, 10000)
        verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)  # type: ignore

        mainLayout = QVBoxLayout()
        mainLayout.addWidget(self.methodLabel)
        mainLayout.addWidget(self.methodComboBox)
        mainLayout.addWidget(self.nSamplesLabel)
        mainLayout.addWidget(self.nSamplesSpinBox)
        mainLayout.addSpacerItem(verticalSpacer)

        self.setLayout(mainLayout)

    def getSamplingSettings(self):
        results = {
            "Method": self.methodComboBox.currentText(),
            "Number of Samples": self.nSamplesSpinBox.value(),
        }
        return results


class SurrogateTab(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.argsList = []
        self.methodLabel = QLabel("Surrogate Method")
        self.methodComboBox = QComboBox()
        self.methodComboBox.addItems(
            [
                "polynomial",
            ]
        )
        degreeFitLabel = QLabel("Degree")
        self.degreeFitSpinBox = QSpinBox()
        self.degreeFitSpinBox.setValue(2)
        interactionOnlyLabel = QLabel("Interaction Only")
        self.interactionOnlyCheckBox = QCheckBox()
        self.interactionOnlyCheckBox.setChecked(False)
        fitInterceptLabel = QLabel("Fit Intercept")
        self.fitInterceptCheckBox = QCheckBox()
        self.fitInterceptCheckBox.setChecked(True)

        verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)  # type: ignore

        self.mainLayout = QVBoxLayout()
        self.mainLayout.addWidget(self.methodLabel)
        self.mainLayout.addWidget(self.methodComboBox)
        self.mainLayout.addWidget(degreeFitLabel)
        self.mainLayout.addWidget(self.degreeFitSpinBox)
        self.mainLayout.addWidget(interactionOnlyLabel)
        self.mainLayout.addWidget(self.interactionOnlyCheckBox)
        self.mainLayout.addWidget(fitInterceptLabel)
        self.mainLayout.addWidget(self.fitInterceptCheckBox)

        self.mainLayout.addSpacerItem(verticalSpacer)

        self.setLayout(self.mainLayout)

    def getSurrogateSettings(self):
        results = {
            "Method": self.methodComboBox.currentText(),
            "Degree of Fit": self.degreeFitSpinBox.value(),
            "Fit Interactions": self.interactionOnlyCheckBox.isChecked(),
            "Fit Intercept": self.fitInterceptCheckBox.isChecked(),
        }
        return results


class OptimizationTab(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.objectiveDefinition = ObjectiveDefinition()
        self.constraintDefinition = ConstraintDefinition()

        self.methodLabel = QLabel("Optimization Algorithm")
        self.methodComboBox = QComboBox()
        self.methodComboBox.addItems(
            ["nsga3", "geneticAlgorithm", "particleSwarm", "nelderMead"]
        )
        self.popSizeLabel = QLabel("Population Size")
        self.popSizeSpinBox = QSpinBox()
        self.popSizeSpinBox.setValue(5)
        self.popSizeSpinBox.setRange(1, 500)

        self.nEvaluationsLabel = QLabel("Number of Evaluations")
        self.nEvaluationsSpinBox = QSpinBox()
        self.nEvaluationsSpinBox.setValue(10)
        self.nEvaluationsSpinBox.setRange(1, 100000)

        self.rankingLabel = QLabel("Ranking Method")
        self.rankingComboBox = QComboBox()
        self.rankingComboBox.addItems(["simpleAdditive", "topsis"])

        verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)  # type: ignore

        optimizationSettingsLayout = QGridLayout()
        optimizationSettingsLayout.addWidget(self.methodLabel, 0, 0)
        optimizationSettingsLayout.addWidget(self.popSizeLabel, 0, 1)
        optimizationSettingsLayout.addWidget(self.nEvaluationsLabel, 0, 2)
        optimizationSettingsLayout.addWidget(self.rankingLabel, 0, 3)

        optimizationSettingsLayout.addWidget(self.methodComboBox, 1, 0)
        optimizationSettingsLayout.addWidget(self.popSizeSpinBox, 1, 1)
        optimizationSettingsLayout.addWidget(self.nEvaluationsSpinBox, 1, 2)
        optimizationSettingsLayout.addWidget(self.rankingComboBox, 1, 3)

        box = QGroupBox()
        box.setTitle("Optimization Settings")
        box.setLayout(optimizationSettingsLayout)

        mainLayout = QVBoxLayout()
        mainLayout.addWidget(box)
        mainLayout.addWidget(self.objectiveDefinition)
        mainLayout.addWidget(self.constraintDefinition)
        mainLayout.addSpacerItem(verticalSpacer)

        self.setLayout(mainLayout)

    def getOptimizationSettings(self):
        objectiveParameters = self.objectiveDefinition.getSettings()
        constraintsParameters = self.constraintDefinition.getSettings()
        results = {
            "Method": self.methodComboBox.currentText(),
            "Population Size": self.popSizeSpinBox.value(),
            "Number of Evaluations": self.nEvaluationsSpinBox.value(),
            "Ranking Method": self.rankingComboBox.currentText(),
            "Objectives Expressions": objectiveParameters,
            "Constraints Expressions": constraintsParameters,
        }
        return results


class App(QDialog):
    def __init__(self) -> None:
        super().__init__()

        self.sidebar = SideBar()
        self.tabs = QTabWidget()
        self.problemTab = ProblemTab()
        self.samplingTab = SamplingTab()
        self.surrogateTab = SurrogateTab()
        self.optimizationTab = OptimizationTab()
        self.tabs.addTab(self.problemTab, "Problem")
        self.tabs.addTab(self.samplingTab, "Sampling")
        self.tabs.addTab(self.surrogateTab, "Surrogate")
        self.tabs.addTab(self.optimizationTab, "Optimisation")
        runButton = QPushButton("Run")
        runButton.clicked.connect(self._runAnalysis)

        mainLayout = QHBoxLayout()
        mainLayout.addWidget(self.sidebar, stretch=3)
        mainLayout.addWidget(self.tabs, stretch=7)
        mainLayout.addWidget(runButton, stretch=1)

        self.resize(809, 500)
        self.setLayout(mainLayout)
        self.setWindowTitle("The Eng")

    def _runAnalysis(self):
        settings = self._getSettings()
        try:
            analysis = TheEng()
            analysis.getSettingsFromDict(settings)
            analysis.run()
        except Exception as e:
            print("Analysis failed.")
            print(e)

    def _getSettings(self):
        sideBarSettings = self.sidebar.getSideBarSettings()
        problemSettings = self.problemTab.getProblemSettings()
        samplingSettings = self.samplingTab.getSamplingSettings()
        surrogateSettings = self.surrogateTab.getSurrogateSettings()
        optimizationSettings = self.optimizationTab.getOptimizationSettings()

        settings = {
            "General Settings": sideBarSettings,
            "Problem": problemSettings,
            "Sampling": samplingSettings,
            "Surrogate": surrogateSettings,
            "Optimization": optimizationSettings,
        }

        with open(
            join(self.sidebar.getWorkingDirectory(), "input.json"), "w"
        ) as outfile:
            dump(settings, outfile)

        print(settings)

        return settings


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    Eng = App()
    Eng.show()
    sys.exit(app.exec())
