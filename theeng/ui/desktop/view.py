import sys
from os.path import join
from os import environ
from json import dump
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

        self.nCpusLabel = QLabel("Number of CPUs")
        self.nCpusSpinBox = QSpinBox()
        self.nCpusSpinBox.setValue(2)

        self.samplingLabel = QLabel("Enable Sampling")
        self.samplingCheckBox = QCheckBox()
        self.samplingCheckBox.setChecked(True)

        self.surrogateLabel = QLabel("Enable Surrogate")
        self.surrogateCheckBox = QCheckBox()
        self.surrogateCheckBox.setChecked(True)

        verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)  # type: ignore

        sidebarLayout = QVBoxLayout()
        sidebarLayout.addWidget(self.workingDirectoryLabel)
        sidebarLayout.addWidget(self.workingDirectoryLine)
        sidebarLayout.addWidget(self.simulationDirectoryLabel)
        sidebarLayout.addWidget(self.simulationDirectoryLine)
        sidebarLayout.addWidget(self.nCpusLabel)
        sidebarLayout.addWidget(self.nCpusSpinBox)
        sidebarLayout.addWidget(self.samplingLabel)
        sidebarLayout.addWidget(self.samplingCheckBox)
        sidebarLayout.addWidget(self.surrogateLabel)
        sidebarLayout.addWidget(self.surrogateCheckBox)
        sidebarLayout.addSpacerItem(verticalSpacer)

        self.setTitle("Global Settings")
        self.setLayout(sidebarLayout)

    def getSideBarSettings(self):
        settings = {
            "Working Directory": self.workingDirectoryLine.text(),
            "Simulation Directory": self.simulationDirectoryLine.text(),
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
        upperBoundDoubleSpinBox = QDoubleSpinBox()
        upperBoundDoubleSpinBox.setValue(0.0)

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
        upperBoundDoubleSpinBox = QDoubleSpinBox()
        upperBoundDoubleSpinBox.setValue(0.0)

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

        resultNameLabel = QLabel("Result Name")
        resultNameLine = QLineEdit()
        resultNameLine.setPlaceholderText("Enter Result name...")

        self.resultNameLines.append(resultNameLine)

        self.resultSettingsLayout = QVBoxLayout()
        self.resultSettingsLayout.addWidget(resultNameLabel)
        self.resultSettingsLayout.addWidget(self.resultNameLines[0])

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
        self.resultNameLines.append(resultNameLine)
        self.resultSettingsLayout.addWidget(self.resultNameLines[-1])

    def removeRow(self):
        self.resultSettingsLayout.removeWidget(self.resultNameLines[-1])
        self.resultNameLines.pop()

    def getResultsSettings(self):
        results = {}
        for resultNameLine in self.resultNameLines:
            results[resultNameLine.text()] = resultNameLine.text()
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

        objectiveNameLabel = QLabel("Objective Expression")
        objectiveNameLine = QLineEdit()
        objectiveNameLine.setPlaceholderText("Enter Objective expression...")

        self.objectiveNameLines.append(objectiveNameLine)

        self.objectiveSettingsLayout = QVBoxLayout()
        self.objectiveSettingsLayout.addWidget(objectiveNameLabel)
        self.objectiveSettingsLayout.addWidget(self.objectiveNameLines[0])

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
        objectiveNameLine.setPlaceholderText("Enter Objective expression...")
        self.objectiveNameLines.append(objectiveNameLine)
        self.objectiveSettingsLayout.addWidget(self.objectiveNameLines[-1])

    def removeRow(self):
        self.objectiveSettingsLayout.removeWidget(self.objectiveNameLines[-1])
        self.objectiveNameLines.pop()

    def getObjectiveSettings(self):
        objectives = {}
        for objectiveNameLine in self.objectiveNameLines:
            objectives[objectiveNameLine.text()] = objectiveNameLine.text()
        return objectives


class ConstraintsDefinition(QGroupBox):
    def __init__(self):
        super().__init__()
        self.constraintNameLines = []

        constraintNameLabel = QLabel("Constraints Expression")
        constraintNameLine = QLineEdit()
        constraintNameLine.setPlaceholderText("Enter Constraints expression...")

        self.constraintNameLines.append(constraintNameLine)

        self.constraintSettingsLayout = QVBoxLayout()
        self.constraintSettingsLayout.addWidget(constraintNameLabel)
        self.constraintSettingsLayout.addWidget(self.constraintNameLines[0])

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
        self.constraintNameLines.append(constraintNameLine)
        self.constraintSettingsLayout.addWidget(self.constraintNameLines[-1])

    def removeRow(self):
        self.constraintSettingsLayout.removeWidget(self.constraintNameLines[-1])
        self.constraintNameLines.pop()

    def getConstraintSettings(self):
        constraints = {}
        for constraintNameLine in self.constraintNameLines:
            constraints[constraintNameLine.text()] = constraintNameLine.text()
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
        self.nEvaluationsLabel = QLabel("Number of Evaluations")
        self.nEvaluationsSpinBox = QSpinBox()
        self.nEvaluationsSpinBox.setValue(10)
        verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)  # type: ignore

        optimizationSettingsLayout = QGridLayout()
        optimizationSettingsLayout.addWidget(self.methodLabel, 0, 0)
        optimizationSettingsLayout.addWidget(self.popSizeLabel, 0, 1)
        optimizationSettingsLayout.addWidget(self.nEvaluationsLabel, 0, 2)
        optimizationSettingsLayout.addWidget(self.methodComboBox, 1, 0)
        optimizationSettingsLayout.addWidget(self.popSizeSpinBox, 1, 1)
        optimizationSettingsLayout.addWidget(self.nEvaluationsSpinBox, 1, 2)

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
        runButton.clicked.connect(self.getSettings)

        mainLayout = QHBoxLayout()
        mainLayout.addWidget(self.sidebar, stretch=3)
        mainLayout.addWidget(self.tabs, stretch=7)
        mainLayout.addWidget(runButton, stretch=1)

        self.resize(809, 500)
        self.setLayout(mainLayout)
        self.setWindowTitle("The Eng")

    def getSettings(self):
        sideBarSettings = self.sidebar.getSideBarSettings()
        problemSettings = self.problemTab.getProblemSettings()
        samplingSettings = self.samplingTab.getSamplingSettings()
        surrogateSettings = self.surrogateTab.getSurrogateSettings()
        optimizationSettings = self.optimizationTab.getOptimizationSettings()

        results = {
            "General Settings": sideBarSettings,
            "Problem": problemSettings,
            "Sampling": samplingSettings,
            "Surrogate": surrogateSettings,
            "Optimization": optimizationSettings,
        }

        with open(join(self.sidebar.getWorkingDirectory(),"input.json"), "w") as outfile:
            dump(results, outfile)

        print(results)

        return results


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    Eng = App()
    Eng.show()
    sys.exit(app.exec())
