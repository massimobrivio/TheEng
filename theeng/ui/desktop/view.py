import sys
from os.path import join
from os import environ
from json import dump
from theeng.theeng import TheEng
from PyQt5.QtWidgets import (
    QApplication,
    QCheckBox,
    QComboBox,
    QDialog,
    QGridLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QSizePolicy,
    QSpinBox,
    QTabWidget,
    QVBoxLayout,
    QWidget,
    QSpacerItem,
    QDoubleSpinBox,
)


class SideBar(QGroupBox):
    def __init__(self):
        super().__init__()
        self.workingDirectoryLabel = QLabel("Working Directory")
        self.workingDirectoryLine = QLineEdit()
        self.workingDirectoryLine.setPlaceholderText("Enter working directory...")
        self.workingDirectoryLine.setText(join(join(environ['USERPROFILE']), 'Desktop') )

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


class ParametersDefinition(QGroupBox):
    def __init__(self):
        super().__init__()
        self.parameterNameLines = []
        self.lowerBoundDoubleSpinBoxes = []
        self.upperBoundDoubleSpinBoxes = []

        ## Parameter Settings Layout

        parameterNameLabel = QLabel("Parameter Name")
        parameterLBoundLabel = QLabel("Lower Bounds")
        parameterUBoundLabel = QLabel("Upper Bounds")

        parameterNameLine = QLineEdit()
        parameterNameLine.setPlaceholderText("Enter parameter name...")
        lowerBoundDoubleSpinBox = QDoubleSpinBox()
        lowerBoundDoubleSpinBox.setValue(0.0)
        lowerBoundDoubleSpinBox.setRange(-1e20, 1e20)
        upperBoundDoubleSpinBox = QDoubleSpinBox()
        upperBoundDoubleSpinBox.setValue(0.0)
        upperBoundDoubleSpinBox.setRange(-1e20, 1e20)

        self.parameterNameLines.append(parameterNameLine)
        self.lowerBoundDoubleSpinBoxes.append(lowerBoundDoubleSpinBox)
        self.upperBoundDoubleSpinBoxes.append(upperBoundDoubleSpinBox)

        self.parameterSettingsLayout = QGridLayout()
        self.parameterSettingsLayout.addWidget(parameterNameLabel, 0, 0)
        self.parameterSettingsLayout.addWidget(parameterLBoundLabel, 0, 1)
        self.parameterSettingsLayout.addWidget(parameterUBoundLabel, 0, 2)

        self.parameterSettingsLayout.addWidget(self.parameterNameLines[0], 1, 0)
        self.parameterSettingsLayout.addWidget(self.lowerBoundDoubleSpinBoxes[0], 1, 1)
        self.parameterSettingsLayout.addWidget(self.upperBoundDoubleSpinBoxes[0], 1, 2)

        ## Add Remove Layout

        self.addClicked = 1
        self.addButton = QPushButton("Add")
        self.addButton.clicked.connect(self.addRow)
        self.removeButton = QPushButton("Remove")
        self.removeButton.clicked.connect(self.removeRow)

        addremoveLayout = QHBoxLayout()
        addremoveLayout.addWidget(self.addButton)
        addremoveLayout.addWidget(self.removeButton)

        ## Overall Layout

        mainLayout = QVBoxLayout()
        mainLayout.addLayout(self.parameterSettingsLayout)
        mainLayout.addLayout(addremoveLayout)

        self.setTitle("Parameter Settings")
        self.setLayout(mainLayout)

    def addRow(self):
        parameterNameLine = QLineEdit()
        parameterNameLine.setPlaceholderText("Enter parameter name...")
        lowerBoundDoubleSpinBox = QDoubleSpinBox()
        lowerBoundDoubleSpinBox.setValue(0.0)
        lowerBoundDoubleSpinBox.setRange(-1e20, 1e20)
        upperBoundDoubleSpinBox = QDoubleSpinBox()
        upperBoundDoubleSpinBox.setValue(0.0)
        upperBoundDoubleSpinBox.setRange(-1e20, 1e20)

        self.parameterNameLines.append(parameterNameLine)
        self.lowerBoundDoubleSpinBoxes.append(lowerBoundDoubleSpinBox)
        self.upperBoundDoubleSpinBoxes.append(upperBoundDoubleSpinBox)

        self.parameterSettingsLayout.addWidget(
            self.parameterNameLines[-1], self.addClicked + 1, 0
        )
        self.parameterSettingsLayout.addWidget(
            self.lowerBoundDoubleSpinBoxes[-1], self.addClicked + 1, 1
        )
        self.parameterSettingsLayout.addWidget(
            self.upperBoundDoubleSpinBoxes[-1], self.addClicked + 1, 2
        )

        self.addClicked += 1

    def removeRow(self):
        self.parameterSettingsLayout.removeWidget(self.parameterNameLines[-1])
        self.parameterSettingsLayout.removeWidget(self.lowerBoundDoubleSpinBoxes[-1])
        self.parameterSettingsLayout.removeWidget(self.upperBoundDoubleSpinBoxes[-1])

        self.parameterNameLines.pop()
        self.lowerBoundDoubleSpinBoxes.pop()
        self.upperBoundDoubleSpinBoxes.pop()

        self.addClicked -= 1

    def getParametersSettings(self):
        results = {}
        for parameterNameLine, lowerBoundDoubleSpinBox, upperBoundDoubleSpinBox in zip(
            self.parameterNameLines,
            self.lowerBoundDoubleSpinBoxes,
            self.upperBoundDoubleSpinBoxes,
        ):
            results[parameterNameLine.text()] = (
                lowerBoundDoubleSpinBox.value(),
                upperBoundDoubleSpinBox.value(),
            )
        return results


class ResultsDefinition(QGroupBox):
    def __init__(self):
        super().__init__()
        self.resultNameLines = []
        self.resultOperationComboBoxes = []

        resultNameLabel = QLabel("Result Name")
        resultNameLine = QLineEdit()
        resultNameLine.setPlaceholderText("Enter Result name...")

        resultOperationLabel = QLabel("Operation")
        resultOperationComboBox = QComboBox()
        resultOperationComboBox.addItems(["None", "Max", "Min", "Avg"])

        self.resultNameLines.append(resultNameLine)
        self.resultOperationComboBoxes.append(resultOperationComboBox)

        self.resultSettingsLayout = QGridLayout()
        self.resultSettingsLayout.addWidget(resultNameLabel, 0, 0)
        self.resultSettingsLayout.addWidget(resultOperationLabel, 0, 1)
        self.resultSettingsLayout.addWidget(self.resultNameLines[0], 1, 0)
        self.resultSettingsLayout.addWidget(self.resultOperationComboBoxes[0], 1, 1)

        self.addClicked = 1
        self.addButton = QPushButton("Add")
        self.addButton.clicked.connect(self.addRow)
        self.removeButton = QPushButton("Remove")
        self.removeButton.clicked.connect(self.removeRow)

        addremoveLayout = QHBoxLayout()
        addremoveLayout.addWidget(self.addButton)
        addremoveLayout.addWidget(self.removeButton)

        ## Overall Layout

        mainLayout = QVBoxLayout()
        mainLayout.addLayout(self.resultSettingsLayout)
        mainLayout.addLayout(addremoveLayout)

        self.setTitle("Results Settings")
        self.setLayout(mainLayout)

    def addRow(self):
        resultNameLine = QLineEdit()
        resultNameLine.setPlaceholderText("Enter Result name...")
        resultOperationComboBox = QComboBox()
        resultOperationComboBox.addItems(["None", "Max", "Min", "Avg"])

        self.resultNameLines.append(resultNameLine)
        self.resultOperationComboBoxes.append(resultOperationComboBox)

        self.resultSettingsLayout.addWidget(self.resultNameLines[-1], self.addClicked + 1, 0)
        self.resultSettingsLayout.addWidget(self.resultOperationComboBoxes[-1], self.addClicked + 1, 1)
        self.addClicked += 1

    def removeRow(self):
        self.resultSettingsLayout.removeWidget(self.resultNameLines[-1])
        self.resultSettingsLayout.removeWidget(self.resultOperationComboBoxes[-1])
        self.resultNameLines.pop()
        self.resultOperationComboBoxes.pop()
        self.addClicked -= 1

    def getResultsSettings(self):
        results = {}
        for resultNameLine, resultOperationComboBox in zip(self.resultNameLines, self.resultOperationComboBoxes):
            results[resultNameLine.text()] = resultOperationComboBox.currentText()
        return results


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
        parameterSettings = self.parametersDefinition.getParametersSettings()
        resultSettings = self.resultsDefinition.getResultsSettings()
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


class ObjectiveDefinition(QGroupBox):
    def __init__(self):
        super().__init__()
        self.objectiveNameLines = []
        self.objectiveWeightsSpinBoxes = []

        ## Parameter Settings Layout

        objectiveNameLabel = QLabel("Objective Expression")
        objectiveWeightLabel = QLabel("Objective Weight")

        objectiveNameLine = QLineEdit()
        objectiveNameLine.setPlaceholderText("Enter Objective Expression...")
        objectiveWeightSpinBox = QDoubleSpinBox()
        objectiveWeightSpinBox.setValue(0.5)
        objectiveWeightSpinBox.setSingleStep(0.1)
        objectiveWeightSpinBox.setRange(0., 1.0)

        self.objectiveNameLines.append(objectiveNameLine)
        self.objectiveWeightsSpinBoxes.append(objectiveWeightSpinBox)

        self.objectiveSettingsLayout = QGridLayout()
        self.objectiveSettingsLayout.addWidget(objectiveNameLabel, 0, 0)
        self.objectiveSettingsLayout.addWidget(objectiveWeightLabel, 0, 1)

        self.objectiveSettingsLayout.addWidget(self.objectiveNameLines[0], 1, 0)
        self.objectiveSettingsLayout.addWidget(self.objectiveWeightsSpinBoxes[0], 1, 1)

        ## Add Remove Layout

        self.addClicked = 1
        self.addButton = QPushButton("Add")
        self.addButton.clicked.connect(self.addRow)
        self.removeButton = QPushButton("Remove")
        self.removeButton.clicked.connect(self.removeRow)

        addremoveLayout = QHBoxLayout()
        addremoveLayout.addWidget(self.addButton)
        addremoveLayout.addWidget(self.removeButton)

        ## Overall Layout

        mainLayout = QVBoxLayout()
        mainLayout.addLayout(self.objectiveSettingsLayout)
        mainLayout.addLayout(addremoveLayout)

        self.setTitle("Objective Settings")
        self.setLayout(mainLayout)

    def addRow(self):
        objectiveNameLine = QLineEdit()
        objectiveNameLine.setPlaceholderText("Enter Objective Expression...")
        objectiveWeightSpinBox = QDoubleSpinBox()
        objectiveWeightSpinBox.setValue(0.5)
        objectiveWeightSpinBox.setSingleStep(0.1)
        objectiveWeightSpinBox.setRange(0., 1.0)

        self.objectiveNameLines.append(objectiveNameLine)
        self.objectiveWeightsSpinBoxes.append(objectiveWeightSpinBox)

        self.objectiveSettingsLayout.addWidget(
            self.objectiveNameLines[-1], self.addClicked + 1, 0
        )
        self.objectiveSettingsLayout.addWidget(
            self.objectiveWeightsSpinBoxes[-1], self.addClicked + 1, 1
        )

        self.addClicked += 1

    def removeRow(self):
        self.objectiveSettingsLayout.removeWidget(self.objectiveNameLines[-1])
        self.objectiveSettingsLayout.removeWidget(self.objectiveWeightsSpinBoxes[-1])

        self.objectiveNameLines.pop()
        self.objectiveWeightsSpinBoxes.pop()

        self.addClicked -= 1

    def getObjectiveSettings(self):
        results = {}
        for objectiveNameLine, objectiveWeightSpinBox in zip(
            self.objectiveNameLines,
            self.objectiveWeightsSpinBoxes,
        ):
            results[objectiveNameLine.text()] = objectiveWeightSpinBox.value()

        return results


class ConstraintsDefinition(QGroupBox):
    def __init__(self):
        super().__init__()
        self.constraintNameLines = []
        self.constraintRelaxationSpinBoxes = []

        constraintNameLabel = QLabel("Constraints Expression")
        constraintRelaxationLabel = QLabel("Constraints Relaxation")

        constraintNameLine = QLineEdit()
        constraintNameLine.setPlaceholderText("Enter Constraints expression...")
        constraintRelaxationSpinBox = QDoubleSpinBox()
        constraintRelaxationSpinBox.setValue(10)
        constraintRelaxationSpinBox.setRange(0., 100)

        self.constraintNameLines.append(constraintNameLine)
        self.constraintRelaxationSpinBoxes.append(constraintRelaxationSpinBox)

        self.constraintSettingsLayout = QGridLayout()
        self.constraintSettingsLayout.addWidget(constraintNameLabel, 0, 0)
        self.constraintSettingsLayout.addWidget(constraintRelaxationLabel, 0, 1)

        self.constraintSettingsLayout.addWidget(self.constraintNameLines[0], 1, 0)
        self.constraintSettingsLayout.addWidget(self.constraintRelaxationSpinBoxes[0], 1, 1)

        self.addClicked = 1
        self.addButton = QPushButton("Add")
        self.addButton.clicked.connect(self.addRow)
        self.removeButton = QPushButton("Remove")
        self.removeButton.clicked.connect(self.removeRow)

        addremoveLayout = QHBoxLayout()
        addremoveLayout.addWidget(self.addButton)
        addremoveLayout.addWidget(self.removeButton)

        ## Overall Layout

        mainLayout = QVBoxLayout()
        mainLayout.addLayout(self.constraintSettingsLayout)
        mainLayout.addLayout(addremoveLayout)

        self.setTitle("Constraints Settings")
        self.setLayout(mainLayout)

    def addRow(self):
        constraintNameLine = QLineEdit()
        constraintNameLine.setPlaceholderText("Enter Constraints expression...")
        constraintRelaxationSpinBox = QDoubleSpinBox()
        constraintRelaxationSpinBox.setValue(10.)
        constraintRelaxationSpinBox.setRange(0., 100)

        self.constraintNameLines.append(constraintNameLine)
        self.constraintRelaxationSpinBoxes.append(constraintRelaxationSpinBox)
        self.constraintSettingsLayout.addWidget(self.constraintNameLines[-1])
        self.constraintSettingsLayout.addWidget(self.constraintRelaxationSpinBoxes[-1])

        self.addClicked += 1

    def removeRow(self):
        self.constraintSettingsLayout.removeWidget(self.constraintNameLines[-1])
        self.constraintSettingsLayout.removeWidget(self.constraintRelaxationSpinBoxes[-1])
        self.constraintNameLines.pop()
        self.constraintRelaxationSpinBoxes.pop()

        self.addClicked -= 1

    def getConstraintSettings(self):
        constraints = {}
        for constraintNameLine, constraintRelaxationSpinBox in zip(self.constraintNameLines, self.constraintRelaxationSpinBoxes):
            constraints[constraintNameLine.text()] = constraintRelaxationSpinBox.value()
        return constraints


class OptimizationTab(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.objectiveDefinition = ObjectiveDefinition()
        self.constraintDefinition = ConstraintsDefinition()

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
        objectiveParameters = self.objectiveDefinition.getObjectiveSettings()
        constraintsParameters = self.constraintDefinition.getConstraintSettings()
        results = {
            "Method": self.methodComboBox.currentText(),
            "Population Size": self.popSizeSpinBox.value(),
            "Number of Evaluations": self.nEvaluationsSpinBox.value(),
            "Ranking Method": self.rankingComboBox.currentText(),
            "Objectives Expressions": objectiveParameters,
            "Constraints Expressions": constraintsParameters
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

        with open(join(self.sidebar.getWorkingDirectory(),"input.json"), "w") as outfile:
            dump(settings, outfile)

        print(settings)

        return settings


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    Eng = App()
    Eng.show()
    sys.exit(app.exec())
