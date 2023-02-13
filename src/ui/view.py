# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'theeng.ui'
#
# Created by: PyQt5 UI code generator 5.15.7
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_TheEng_MainWindow(object):
    def setupUi(self, TheEng_MainWindow):
        TheEng_MainWindow.setObjectName("TheEng_MainWindow")
        TheEng_MainWindow.resize(1000, 600)
        self.centralwidget = QtWidgets.QWidget(TheEng_MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.sidebarWidget = QtWidgets.QWidget(self.centralwidget)
        self.sidebarWidget.setObjectName("sidebarWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.sidebarWidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(self.sidebarWidget)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        spacerItem = QtWidgets.QSpacerItem(
            40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum
        )
        self.horizontalLayout.addItem(spacerItem)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.pathLabel = QtWidgets.QLabel(self.sidebarWidget)
        font = QtGui.QFont()
        font.setBold(False)
        font.setItalic(True)
        font.setWeight(50)
        self.pathLabel.setFont(font)
        self.pathLabel.setObjectName("pathLabel")
        self.verticalLayout.addWidget(self.pathLabel)
        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setObjectName("formLayout")
        self.fcLabel = QtWidgets.QLabel(self.sidebarWidget)
        self.fcLabel.setObjectName("fcLabel")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.fcLabel)
        self.fcLineEdit = QtWidgets.QLineEdit(self.sidebarWidget)
        self.fcLineEdit.setObjectName("fcLineEdit")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.fcLineEdit)
        self.wdLabel = QtWidgets.QLabel(self.sidebarWidget)
        self.wdLabel.setObjectName("wdLabel")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.wdLabel)
        self.wdLineEdit = QtWidgets.QLineEdit(self.sidebarWidget)
        self.wdLineEdit.setText("")
        self.wdLineEdit.setObjectName("wdLineEdit")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.wdLineEdit)
        self.verticalLayout.addLayout(self.formLayout)
        self.line = QtWidgets.QFrame(self.sidebarWidget)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.verticalLayout.addWidget(self.line)
        self.simulationLabel = QtWidgets.QLabel(self.sidebarWidget)
        font = QtGui.QFont()
        font.setBold(False)
        font.setItalic(True)
        font.setWeight(50)
        self.simulationLabel.setFont(font)
        self.simulationLabel.setObjectName("simulationLabel")
        self.verticalLayout.addWidget(self.simulationLabel)
        self.formLayout_2 = QtWidgets.QFormLayout()
        self.formLayout_2.setObjectName("formLayout_2")
        self.resultLabel = QtWidgets.QLabel(self.sidebarWidget)
        self.resultLabel.setObjectName("resultLabel")
        self.formLayout_2.setWidget(
            0, QtWidgets.QFormLayout.LabelRole, self.resultLabel
        )
        self.resultLineEdit = QtWidgets.QLineEdit(self.sidebarWidget)
        self.resultLineEdit.setObjectName("resultLineEdit")
        self.formLayout_2.setWidget(
            0, QtWidgets.QFormLayout.FieldRole, self.resultLineEdit
        )
        self.cpuLabel = QtWidgets.QLabel(self.sidebarWidget)
        self.cpuLabel.setObjectName("cpuLabel")
        self.formLayout_2.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.cpuLabel)
        self.cpuSpinBox = QtWidgets.QSpinBox(self.sidebarWidget)
        self.cpuSpinBox.setMinimum(1)
        self.cpuSpinBox.setObjectName("cpuSpinBox")
        self.formLayout_2.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.cpuSpinBox)
        self.verticalLayout.addLayout(self.formLayout_2)
        spacerItem1 = QtWidgets.QSpacerItem(
            20, 345, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding
        )
        self.verticalLayout.addItem(spacerItem1)
        self.runLayuot = QtWidgets.QHBoxLayout()
        self.runLayuot.setObjectName("runLayuot")
        spacerItem2 = QtWidgets.QSpacerItem(
            40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum
        )
        self.runLayuot.addItem(spacerItem2)
        self.runButton = QtWidgets.QPushButton(self.sidebarWidget)
        self.runButton.setObjectName("runButton")
        self.runLayuot.addWidget(self.runButton)
        spacerItem3 = QtWidgets.QSpacerItem(
            40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum
        )
        self.runLayuot.addItem(spacerItem3)
        self.verticalLayout.addLayout(self.runLayuot)
        self.horizontalLayout_3.addWidget(self.sidebarWidget)
        self.verticalLayout_13 = QtWidgets.QVBoxLayout()
        self.verticalLayout_13.setObjectName("verticalLayout_13")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setTabPosition(QtWidgets.QTabWidget.North)
        self.tabWidget.setObjectName("tabWidget")
        self.problem_tab = QtWidgets.QWidget()
        self.problem_tab.setObjectName("problem_tab")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.problem_tab)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.designvariableLabel = QtWidgets.QLabel(self.problem_tab)
        self.designvariableLabel.setObjectName("designvariableLabel")
        self.verticalLayout_3.addWidget(self.designvariableLabel)
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.label_3 = QtWidgets.QLabel(self.problem_tab)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 0, 0, 1, 1)
        self.doubleSpinBox_2 = QtWidgets.QDoubleSpinBox(self.problem_tab)
        self.doubleSpinBox_2.setObjectName("doubleSpinBox_2")
        self.gridLayout.addWidget(self.doubleSpinBox_2, 1, 2, 1, 1)
        self.label_6 = QtWidgets.QLabel(self.problem_tab)
        self.label_6.setObjectName("label_6")
        self.gridLayout.addWidget(self.label_6, 0, 2, 1, 1)
        self.label_5 = QtWidgets.QLabel(self.problem_tab)
        self.label_5.setObjectName("label_5")
        self.gridLayout.addWidget(self.label_5, 0, 1, 1, 1)
        self.doubleSpinBox = QtWidgets.QDoubleSpinBox(self.problem_tab)
        self.doubleSpinBox.setSpecialValueText("")
        self.doubleSpinBox.setObjectName("doubleSpinBox")
        self.gridLayout.addWidget(self.doubleSpinBox, 1, 1, 1, 1)
        self.lineEdit = QtWidgets.QLineEdit(self.problem_tab)
        self.lineEdit.setObjectName("lineEdit")
        self.gridLayout.addWidget(self.lineEdit, 1, 0, 1, 1)
        self.gridLayout.setColumnStretch(0, 1)
        self.verticalLayout_3.addLayout(self.gridLayout)
        self.line_2 = QtWidgets.QFrame(self.problem_tab)
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.verticalLayout_3.addWidget(self.line_2)
        self.objectiveLabel = QtWidgets.QLabel(self.problem_tab)
        self.objectiveLabel.setObjectName("objectiveLabel")
        self.verticalLayout_3.addWidget(self.objectiveLabel)
        self.expressionLabel = QtWidgets.QLabel(self.problem_tab)
        self.expressionLabel.setObjectName("expressionLabel")
        self.verticalLayout_3.addWidget(self.expressionLabel)
        self.lineEdit_2 = QtWidgets.QLineEdit(self.problem_tab)
        self.lineEdit_2.setText("")
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.verticalLayout_3.addWidget(self.lineEdit_2)
        self.verticalLayout_5.addLayout(self.verticalLayout_3)
        icon = QtGui.QIcon()
        icon.addPixmap(
            QtGui.QPixmap(":/icons/icons/problem_sidebar.png"),
            QtGui.QIcon.Normal,
            QtGui.QIcon.Off,
        )
        self.tabWidget.addTab(self.problem_tab, icon, "")
        self.sampling_tab = QtWidgets.QWidget()
        self.sampling_tab.setObjectName("sampling_tab")
        self.verticalLayout_7 = QtWidgets.QVBoxLayout(self.sampling_tab)
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout()
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.widget_2 = QtWidgets.QWidget(self.sampling_tab)
        self.widget_2.setObjectName("widget_2")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.widget_2)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.spinBox = QtWidgets.QSpinBox(self.widget_2)
        self.spinBox.setMinimum(2)
        self.spinBox.setMaximum(100000)
        self.spinBox.setProperty("value", 50)
        self.spinBox.setObjectName("spinBox")
        self.gridLayout_3.addWidget(self.spinBox, 0, 1, 1, 1)
        self.label_9 = QtWidgets.QLabel(self.widget_2)
        self.label_9.setObjectName("label_9")
        self.gridLayout_3.addWidget(self.label_9, 0, 0, 1, 1)
        self.lineEdit_3 = QtWidgets.QLineEdit(self.widget_2)
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.gridLayout_3.addWidget(self.lineEdit_3, 1, 1, 1, 1)
        self.label_10 = QtWidgets.QLabel(self.widget_2)
        self.label_10.setObjectName("label_10")
        self.gridLayout_3.addWidget(self.label_10, 1, 0, 1, 1)
        self.gridLayout_3.setColumnStretch(0, 1)
        self.gridLayout_3.setColumnStretch(1, 1)
        self.verticalLayout_6.addWidget(self.widget_2)
        spacerItem4 = QtWidgets.QSpacerItem(
            20, 118, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding
        )
        self.verticalLayout_6.addItem(spacerItem4)
        self.verticalLayout_7.addLayout(self.verticalLayout_6)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(
            QtGui.QPixmap(":/icons/icons/sampling_sidebar.png"),
            QtGui.QIcon.Normal,
            QtGui.QIcon.Off,
        )
        self.tabWidget.addTab(self.sampling_tab, icon1, "")
        self.surrogate_tab = QtWidgets.QWidget()
        self.surrogate_tab.setObjectName("surrogate_tab")
        self.verticalLayout_8 = QtWidgets.QVBoxLayout(self.surrogate_tab)
        self.verticalLayout_8.setObjectName("verticalLayout_8")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.gridLayout_4 = QtWidgets.QGridLayout()
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.label_11 = QtWidgets.QLabel(self.surrogate_tab)
        self.label_11.setObjectName("label_11")
        self.gridLayout_4.addWidget(self.label_11, 0, 0, 1, 1)
        self.lineEdit_4 = QtWidgets.QLineEdit(self.surrogate_tab)
        self.lineEdit_4.setObjectName("lineEdit_4")
        self.gridLayout_4.addWidget(self.lineEdit_4, 0, 1, 1, 1)
        self.label_12 = QtWidgets.QLabel(self.surrogate_tab)
        self.label_12.setObjectName("label_12")
        self.gridLayout_4.addWidget(self.label_12, 1, 0, 1, 1)
        self.spinBox_2 = QtWidgets.QSpinBox(self.surrogate_tab)
        self.spinBox_2.setMinimum(1)
        self.spinBox_2.setProperty("value", 2)
        self.spinBox_2.setObjectName("spinBox_2")
        self.gridLayout_4.addWidget(self.spinBox_2, 1, 1, 1, 1)
        self.gridLayout_4.setColumnStretch(0, 1)
        self.gridLayout_4.setColumnStretch(1, 1)
        self.verticalLayout_2.addLayout(self.gridLayout_4)
        spacerItem5 = QtWidgets.QSpacerItem(
            20, 128, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding
        )
        self.verticalLayout_2.addItem(spacerItem5)
        self.verticalLayout_8.addLayout(self.verticalLayout_2)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(
            QtGui.QPixmap(":/icons/icons/surrogate_sidebar.png"),
            QtGui.QIcon.Normal,
            QtGui.QIcon.Off,
        )
        self.tabWidget.addTab(self.surrogate_tab, icon2, "")
        self.optimization_tab = QtWidgets.QWidget()
        self.optimization_tab.setObjectName("optimization_tab")
        self.verticalLayout_10 = QtWidgets.QVBoxLayout(self.optimization_tab)
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.verticalLayout_9 = QtWidgets.QVBoxLayout()
        self.verticalLayout_9.setObjectName("verticalLayout_9")
        self.gridLayout_5 = QtWidgets.QGridLayout()
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.label_13 = QtWidgets.QLabel(self.optimization_tab)
        self.label_13.setObjectName("label_13")
        self.gridLayout_5.addWidget(self.label_13, 0, 0, 1, 1)
        self.lineEdit_5 = QtWidgets.QLineEdit(self.optimization_tab)
        self.lineEdit_5.setObjectName("lineEdit_5")
        self.gridLayout_5.addWidget(self.lineEdit_5, 0, 1, 1, 1)
        self.label_14 = QtWidgets.QLabel(self.optimization_tab)
        self.label_14.setObjectName("label_14")
        self.gridLayout_5.addWidget(self.label_14, 1, 0, 1, 1)
        self.spinBox_3 = QtWidgets.QSpinBox(self.optimization_tab)
        self.spinBox_3.setObjectName("spinBox_3")
        self.gridLayout_5.addWidget(self.spinBox_3, 1, 1, 1, 1)
        self.label_15 = QtWidgets.QLabel(self.optimization_tab)
        self.label_15.setObjectName("label_15")
        self.gridLayout_5.addWidget(self.label_15, 2, 0, 1, 1)
        self.spinBox_4 = QtWidgets.QSpinBox(self.optimization_tab)
        self.spinBox_4.setObjectName("spinBox_4")
        self.gridLayout_5.addWidget(self.spinBox_4, 2, 1, 1, 1)
        self.gridLayout_5.setColumnStretch(0, 1)
        self.gridLayout_5.setColumnStretch(1, 1)
        self.verticalLayout_9.addLayout(self.gridLayout_5)
        spacerItem6 = QtWidgets.QSpacerItem(
            20, 108, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding
        )
        self.verticalLayout_9.addItem(spacerItem6)
        self.verticalLayout_10.addLayout(self.verticalLayout_9)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(
            QtGui.QPixmap(":/icons/icons/optimization_sidebar.png"),
            QtGui.QIcon.Normal,
            QtGui.QIcon.Off,
        )
        self.tabWidget.addTab(self.optimization_tab, icon3, "")
        self.verticalLayout_13.addWidget(self.tabWidget)
        self.serialWidget = QtWidgets.QWidget(self.centralwidget)
        self.serialWidget.setObjectName("serialWidget")
        self.verticalLayout_12 = QtWidgets.QVBoxLayout(self.serialWidget)
        self.verticalLayout_12.setObjectName("verticalLayout_12")
        self.verticalLayout_11 = QtWidgets.QVBoxLayout()
        self.verticalLayout_11.setObjectName("verticalLayout_11")
        self.label_2 = QtWidgets.QLabel(self.serialWidget)
        self.label_2.setObjectName("label_2")
        self.verticalLayout_11.addWidget(self.label_2)
        self.textEdit = QtWidgets.QTextEdit(self.serialWidget)
        self.textEdit.setReadOnly(True)
        self.textEdit.setObjectName("textEdit")
        self.verticalLayout_11.addWidget(self.textEdit)
        self.verticalLayout_12.addLayout(self.verticalLayout_11)
        self.verticalLayout_13.addWidget(self.serialWidget)
        self.verticalLayout_13.setStretch(0, 3)
        self.verticalLayout_13.setStretch(1, 2)
        self.horizontalLayout_3.addLayout(self.verticalLayout_13)
        self.horizontalLayout_3.setStretch(0, 1)
        self.horizontalLayout_3.setStretch(1, 3)
        self.verticalLayout_4.addLayout(self.horizontalLayout_3)
        TheEng_MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(TheEng_MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(TheEng_MainWindow)

    def retranslateUi(self, TheEng_MainWindow):
        _translate = QtCore.QCoreApplication.translate
        TheEng_MainWindow.setWindowTitle(_translate("TheEng_MainWindow", "MainWindow"))
        self.label.setText(_translate("TheEng_MainWindow", "General Settings"))
        self.pathLabel.setText(_translate("TheEng_MainWindow", "Paths"))
        self.fcLabel.setText(_translate("TheEng_MainWindow", "FreeCAD Model"))
        self.fcLineEdit.setPlaceholderText(_translate("TheEng_MainWindow", "C:\\"))
        self.wdLabel.setText(_translate("TheEng_MainWindow", "Working Directory"))
        self.wdLineEdit.setPlaceholderText(_translate("TheEng_MainWindow", "C:\\"))
        self.simulationLabel.setText(_translate("TheEng_MainWindow", "Simulation"))
        self.resultLabel.setText(_translate("TheEng_MainWindow", "Result list"))
        self.resultLineEdit.setPlaceholderText(
            _translate("TheEng_MainWindow", "Displacement")
        )
        self.cpuLabel.setText(_translate("TheEng_MainWindow", "CPU number"))
        self.runButton.setText(_translate("TheEng_MainWindow", "Run"))
        self.designvariableLabel.setText(
            _translate("TheEng_MainWindow", "Design Variables")
        )
        self.label_3.setText(_translate("TheEng_MainWindow", "Name"))
        self.label_6.setText(_translate("TheEng_MainWindow", "Upper Bound"))
        self.label_5.setText(_translate("TheEng_MainWindow", "Lower Bound"))
        self.objectiveLabel.setText(_translate("TheEng_MainWindow", "Objectives"))
        self.expressionLabel.setText(_translate("TheEng_MainWindow", "Expressions"))
        self.lineEdit_2.setPlaceholderText(
            _translate("TheEng_MainWindow", "Disolacement^2")
        )
        self.tabWidget.setTabText(
            self.tabWidget.indexOf(self.problem_tab),
            _translate("TheEng_MainWindow", "Problem"),
        )
        self.label_9.setText(_translate("TheEng_MainWindow", "Number of Samples"))
        self.lineEdit_3.setText(_translate("TheEng_MainWindow", "Latin"))
        self.lineEdit_3.setPlaceholderText(_translate("TheEng_MainWindow", "Latin"))
        self.label_10.setText(_translate("TheEng_MainWindow", "Sampling Method"))
        self.tabWidget.setTabText(
            self.tabWidget.indexOf(self.sampling_tab),
            _translate("TheEng_MainWindow", "Sampling"),
        )
        self.label_11.setText(_translate("TheEng_MainWindow", "Method"))
        self.lineEdit_4.setText(_translate("TheEng_MainWindow", "polynomial"))
        self.lineEdit_4.setPlaceholderText(
            _translate("TheEng_MainWindow", "polynomial")
        )
        self.label_12.setText(_translate("TheEng_MainWindow", "Degree Fit"))
        self.tabWidget.setTabText(
            self.tabWidget.indexOf(self.surrogate_tab),
            _translate("TheEng_MainWindow", "Surrogate"),
        )
        self.label_13.setText(_translate("TheEng_MainWindow", "Method"))
        self.label_14.setText(_translate("TheEng_MainWindow", "Population Size"))
        self.label_15.setText(_translate("TheEng_MainWindow", "Number of Evaluations"))
        self.tabWidget.setTabText(
            self.tabWidget.indexOf(self.optimization_tab),
            _translate("TheEng_MainWindow", "Optimization"),
        )
        self.label_2.setText(_translate("TheEng_MainWindow", "Serial Output"))


import resources_rc


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    TheEng_MainWindow = QtWidgets.QMainWindow()
    ui = Ui_TheEng_MainWindow()
    ui.setupUi(TheEng_MainWindow)
    TheEng_MainWindow.show()
    sys.exit(app.exec_())