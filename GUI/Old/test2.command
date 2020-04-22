#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'test.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_CameraRobot(object):
    def setupUi(self, CameraRobot):
        CameraRobot.setObjectName("CameraRobot")
        CameraRobot.resize(720, 480)
        CameraRobot.setToolTipDuration(0)
        self.entireFrame = QtWidgets.QFrame(CameraRobot)
        self.entireFrame.setGeometry(QtCore.QRect(0, 0, 721, 481))
        self.entireFrame.setAutoFillBackground(True)
        self.entireFrame.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.entireFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.entireFrame.setLineWidth(1)
        self.entireFrame.setMidLineWidth(0)
        self.entireFrame.setObjectName("entireFrame")
        self.systemModeFrame = QtWidgets.QFrame(self.entireFrame)
        self.systemModeFrame.setGeometry(QtCore.QRect(50, 70, 181, 51))
        self.systemModeFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.systemModeFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.systemModeFrame.setObjectName("systemModeFrame")
        self.systemModeMenu = QtWidgets.QComboBox(self.systemModeFrame)
        self.systemModeMenu.setGeometry(QtCore.QRect(20, 20, 141, 26))
        self.systemModeMenu.setEditable(False)
        self.systemModeMenu.setMaxVisibleItems(10)
        self.systemModeMenu.setMinimumContentsLength(1)
        self.systemModeMenu.setObjectName("systemModeMenu")
        self.systemModeMenu.addItem("")
        self.systemModeMenu.addItem("")
        self.systemModeMenu.addItem("")
        self.systemModeMenu.addItem("")
        self.systemModeLabel = QtWidgets.QLabel(self.systemModeFrame)
        self.systemModeLabel.setGeometry(QtCore.QRect(0, 0, 181, 20))
        self.systemModeLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.systemModeLabel.setObjectName("systemModeLabel")
        self.repeatPathButtons = QtWidgets.QFrame(self.entireFrame)
        self.repeatPathButtons.setGeometry(QtCore.QRect(50, 120, 181, 111))
        self.repeatPathButtons.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.repeatPathButtons.setFrameShadow(QtWidgets.QFrame.Raised)
        self.repeatPathButtons.setObjectName("repeatPathButtons")
        self.startRecording = QtWidgets.QPushButton(self.repeatPathButtons)
        self.startRecording.setGeometry(QtCore.QRect(30, 10, 121, 31))
        self.startRecording.setAutoDefault(False)
        self.startRecording.setObjectName("startRecording")
        self.stopRecording = QtWidgets.QPushButton(self.repeatPathButtons)
        self.stopRecording.setGeometry(QtCore.QRect(30, 40, 121, 31))
        self.stopRecording.setAutoDefault(False)
        self.stopRecording.setObjectName("stopRecording")
        self.returnToHome = QtWidgets.QPushButton(self.repeatPathButtons)
        self.returnToHome.setGeometry(QtCore.QRect(30, 70, 121, 31))
        self.returnToHome.setAutoDefault(False)
        self.returnToHome.setObjectName("returnToHome")
        self.objectDetectionFrame = QtWidgets.QFrame(self.entireFrame)
        self.objectDetectionFrame.setGeometry(QtCore.QRect(50, 230, 181, 61))
        self.objectDetectionFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.objectDetectionFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.objectDetectionFrame.setObjectName("objectDetectionFrame")
        self.objectDetection = QtWidgets.QCheckBox(self.objectDetectionFrame)
        self.objectDetection.setGeometry(QtCore.QRect(0, 0, 181, 20))
        self.objectDetection.setChecked(True)
        self.objectDetection.setTristate(False)
        self.objectDetection.setObjectName("objectDetection")
        self.textBrowser = QtWidgets.QTextBrowser(self.objectDetectionFrame)
        self.textBrowser.setGeometry(QtCore.QRect(20, 20, 141, 31))
        self.textBrowser.setMidLineWidth(0)
        self.textBrowser.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustIgnored)
        self.textBrowser.setDocumentTitle("")
        self.textBrowser.setTextInteractionFlags(QtCore.Qt.NoTextInteraction)
        self.textBrowser.setObjectName("textBrowser")
        self.maxSpeedFrame = QtWidgets.QFrame(self.entireFrame)
        self.maxSpeedFrame.setGeometry(QtCore.QRect(230, 70, 181, 51))
        self.maxSpeedFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.maxSpeedFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.maxSpeedFrame.setObjectName("maxSpeedFrame")
        self.maxSpeed = QtWidgets.QDoubleSpinBox(self.maxSpeedFrame)
        self.maxSpeed.setGeometry(QtCore.QRect(50, 20, 81, 24))
        self.maxSpeed.setAlignment(QtCore.Qt.AlignCenter)
        self.maxSpeed.setButtonSymbols(QtWidgets.QAbstractSpinBox.UpDownArrows)
        self.maxSpeed.setProperty("showGroupSeparator", False)
        self.maxSpeed.setDecimals(1)
        self.maxSpeed.setMaximum(5.0)
        self.maxSpeed.setSingleStep(0.1)
        self.maxSpeed.setObjectName("maxSpeed")
        self.maxSpeedLabel = QtWidgets.QLabel(self.maxSpeedFrame)
        self.maxSpeedLabel.setGeometry(QtCore.QRect(0, 0, 181, 20))
        self.maxSpeedLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.maxSpeedLabel.setObjectName("maxSpeedLabel")

        self.retranslateUi(CameraRobot)
        self.systemModeMenu.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(CameraRobot)

    def retranslateUi(self, CameraRobot):
        _translate = QtCore.QCoreApplication.translate
        CameraRobot.setWindowTitle(_translate("CameraRobot", "360º Camera Robot"))
        self.systemModeMenu.setCurrentText(_translate("CameraRobot", "Controller"))
        self.systemModeMenu.setItemText(0, _translate("CameraRobot", "Controller"))
        self.systemModeMenu.setItemText(1, _translate("CameraRobot", "Repeat Path"))
        self.systemModeMenu.setItemText(2, _translate("CameraRobot", "Digital Joystick"))
        self.systemModeMenu.setItemText(3, _translate("CameraRobot", "Line Following"))
        self.systemModeLabel.setText(_translate("CameraRobot", "System Mode"))
        self.startRecording.setText(_translate("CameraRobot", "Start Recording"))
        self.stopRecording.setText(_translate("CameraRobot", "Stop Recording"))
        self.returnToHome.setText(_translate("CameraRobot", "Return to Home"))
        self.objectDetection.setText(_translate("CameraRobot", "   Enable Object Detection"))
        self.textBrowser.setPlaceholderText(_translate("CameraRobot", "Distance to Object"))
        self.maxSpeed.setSuffix(_translate("CameraRobot", " mph"))
        self.maxSpeedLabel.setText(_translate("CameraRobot", "Max Speed:"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    CameraRobot = QtWidgets.QDialog()
    ui = Ui_CameraRobot()
    ui.setupUi(CameraRobot)
    CameraRobot.show()
    sys.exit(app.exec_())