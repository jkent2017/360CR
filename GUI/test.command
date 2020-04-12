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
        CameraRobot.setAutoFillBackground(False)
        CameraRobot.setSizeGripEnabled(False)
        CameraRobot.setModal(False)
        self.entireFrame = QtWidgets.QFrame(CameraRobot)
        self.entireFrame.setGeometry(QtCore.QRect(0, 0, 721, 481))
        self.entireFrame.setAutoFillBackground(True)
        self.entireFrame.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.entireFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.entireFrame.setLineWidth(1)
        self.entireFrame.setMidLineWidth(0)
        self.entireFrame.setObjectName("entireFrame")
        self.repeatPathButtons = QtWidgets.QFrame(self.entireFrame)
        self.repeatPathButtons.setGeometry(QtCore.QRect(120, 0, 271, 71))
        self.repeatPathButtons.setAutoFillBackground(True)
        self.repeatPathButtons.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.repeatPathButtons.setFrameShadow(QtWidgets.QFrame.Raised)
        self.repeatPathButtons.setObjectName("repeatPathButtons")
        self.startRecording = QtWidgets.QPushButton(self.repeatPathButtons)
        self.startRecording.setGeometry(QtCore.QRect(10, 10, 120, 30))
        self.startRecording.setAutoDefault(False)
        self.startRecording.setObjectName("startRecording")
        self.stopRecording = QtWidgets.QPushButton(self.repeatPathButtons)
        self.stopRecording.setGeometry(QtCore.QRect(10, 40, 120, 30))
        self.stopRecording.setAutoDefault(False)
        self.stopRecording.setObjectName("stopRecording")
        self.returnToHome = QtWidgets.QPushButton(self.repeatPathButtons)
        self.returnToHome.setGeometry(QtCore.QRect(140, 10, 120, 30))
        self.returnToHome.setAutoDefault(False)
        self.returnToHome.setObjectName("returnToHome")
        self.traversePath = QtWidgets.QPushButton(self.repeatPathButtons)
        self.traversePath.setGeometry(QtCore.QRect(140, 40, 120, 30))
        self.traversePath.setAutoDefault(False)
        self.traversePath.setObjectName("traversePath")
        self.returnToHome.raise_()
        self.startRecording.raise_()
        self.stopRecording.raise_()
        self.traversePath.raise_()
        self.maxSpeedFrame = QtWidgets.QFrame(self.entireFrame)
        self.maxSpeedFrame.setGeometry(QtCore.QRect(0, 0, 121, 71))
        self.maxSpeedFrame.setAutoFillBackground(True)
        self.maxSpeedFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.maxSpeedFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.maxSpeedFrame.setObjectName("maxSpeedFrame")
        self.maxSpeed = QtWidgets.QDoubleSpinBox(self.maxSpeedFrame)
        self.maxSpeed.setGeometry(QtCore.QRect(20, 30, 81, 24))
        self.maxSpeed.setAlignment(QtCore.Qt.AlignCenter)
        self.maxSpeed.setButtonSymbols(QtWidgets.QAbstractSpinBox.UpDownArrows)
        self.maxSpeed.setProperty("showGroupSeparator", False)
        self.maxSpeed.setDecimals(1)
        self.maxSpeed.setMaximum(5.0)
        self.maxSpeed.setSingleStep(0.1)
        self.maxSpeed.setObjectName("maxSpeed")
        self.maxSpeedLabel = QtWidgets.QLabel(self.maxSpeedFrame)
        self.maxSpeedLabel.setGeometry(QtCore.QRect(0, 10, 121, 20))
        self.maxSpeedLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.maxSpeedLabel.setObjectName("maxSpeedLabel")
        self.LiveFeed = QtWidgets.QFrame(self.entireFrame)
        self.LiveFeed.setGeometry(QtCore.QRect(0, 70, 721, 411))
        self.LiveFeed.setToolTipDuration(0)
        self.LiveFeed.setAutoFillBackground(True)
        self.LiveFeed.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.LiveFeed.setFrameShadow(QtWidgets.QFrame.Raised)
        self.LiveFeed.setObjectName("LiveFeed")
        self.frame = QtWidgets.QFrame(self.entireFrame)
        self.frame.setGeometry(QtCore.QRect(390, 0, 331, 71))
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.TCPLogScroll = QtWidgets.QTextBrowser(self.frame)
        self.TCPLogScroll.setGeometry(QtCore.QRect(0, 20, 331, 21))
        self.TCPLogScroll.setAutoFillBackground(True)
        self.TCPLogScroll.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.TCPLogScroll.setOpenLinks(False)
        self.TCPLogScroll.setObjectName("TCPLogScroll")
        self.LogMessage = QtWidgets.QTextBrowser(self.frame)
        self.LogMessage.setGeometry(QtCore.QRect(0, 0, 331, 21))
        self.LogMessage.setAutoFillBackground(True)
        self.LogMessage.setObjectName("LogMessage")
        self.TCPLogStatic = QtWidgets.QLabel(self.frame)
        self.TCPLogStatic.setGeometry(QtCore.QRect(0, 40, 331, 31))
        self.TCPLogStatic.setObjectName("TCPLogStatic")

        self.retranslateUi(CameraRobot)
        self.startRecording.clicked.connect(self._startRecording)
        self.stopRecording.clicked.connect(self._stopRecording)
        self.returnToHome.clicked.connect(self._returnToHome)
        self.traversePath.clicked.connect(self._traversePath)
        QtCore.QMetaObject.connectSlotsByName(CameraRobot)

    def retranslateUi(self, CameraRobot):
        _translate = QtCore.QCoreApplication.translate
        CameraRobot.setWindowTitle(_translate("CameraRobot", "360º Camera Robot"))
        self.startRecording.setText(_translate("CameraRobot", "Start Recording"))
        self.stopRecording.setText(_translate("CameraRobot", "Stop Recording"))
        self.returnToHome.setText(_translate("CameraRobot", "Return to Home"))
        self.traversePath.setText(_translate("CameraRobot", "Traverse Path"))
        self.maxSpeed.setSuffix(_translate("CameraRobot", " mph"))
        self.maxSpeedLabel.setText(_translate("CameraRobot", "Max Speed:"))
        self.LogMessage.setHtml(_translate("CameraRobot", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'.AppleSystemUIFont\'; font-size:13pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:14pt;\">TCP Log:</span></p></body></html>"))
        self.TCPLogStatic.setText(_translate("CameraRobot", "Test Message"))

    def _startRecording(self):
        print("Started Recording.")

    def _stopRecording(self):
        print("Stopped Recording.")

    def _returnToHome(self):
        print("Returning to home.")

    def _traversePath(self):
        print("Traversing Path.")

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    CameraRobot = QtWidgets.QDialog()
    ui = Ui_CameraRobot()
    ui.setupUi(CameraRobot)
    CameraRobot.show()
    sys.exit(app.exec_())
