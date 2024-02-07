# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mainGUIwrLLXo.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

from . import happynserver_rc

class Ui_HappynServerWindow(object):
    def setupUi(self, HappynServerWindow):
        if not HappynServerWindow.objectName():
            HappynServerWindow.setObjectName(u"HappynServerWindow")
        HappynServerWindow.setWindowModality(Qt.NonModal)
        HappynServerWindow.resize(600, 800)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(HappynServerWindow.sizePolicy().hasHeightForWidth())
        HappynServerWindow.setSizePolicy(sizePolicy)
        HappynServerWindow.setMinimumSize(QSize(600, 800))
        HappynServerWindow.setMaximumSize(QSize(600, 800))
        icon = QIcon()
        icon.addFile(u":/icons/icon144.png", QSize(), QIcon.Normal, QIcon.Off)
        icon.addFile(u":/icons/icon144.png", QSize(), QIcon.Normal, QIcon.On)
        HappynServerWindow.setWindowIcon(icon)
        self.centralwidget = QWidget(HappynServerWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayoutWidget = QWidget(self.centralwidget)
        self.verticalLayoutWidget.setObjectName(u"verticalLayoutWidget")
        self.verticalLayoutWidget.setGeometry(QRect(10, 0, 581, 151))
        self.verticalLayoutNetSetting = QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayoutNetSetting.setObjectName(u"verticalLayoutNetSetting")
        self.verticalLayoutNetSetting.setContentsMargins(0, 0, 0, 0)
        self.groupBoxSetting = QGroupBox(self.verticalLayoutWidget)
        self.groupBoxSetting.setObjectName(u"groupBoxSetting")
        sizePolicy1 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.groupBoxSetting.sizePolicy().hasHeightForWidth())
        self.groupBoxSetting.setSizePolicy(sizePolicy1)
        self.layoutWidget = QWidget(self.groupBoxSetting)
        self.layoutWidget.setObjectName(u"layoutWidget")
        self.layoutWidget.setGeometry(QRect(10, 30, 561, 88))
        self.gridLayout = QGridLayout(self.layoutWidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.labelServerPort = QLabel(self.layoutWidget)
        self.labelServerPort.setObjectName(u"labelServerPort")

        self.gridLayout.addWidget(self.labelServerPort, 0, 0, 1, 1)

        self.lineServerPort = QLineEdit(self.layoutWidget)
        self.lineServerPort.setObjectName(u"lineServerPort")

        self.gridLayout.addWidget(self.lineServerPort, 0, 1, 1, 1)

        self.labelServerID = QLabel(self.layoutWidget)
        self.labelServerID.setObjectName(u"labelServerID")

        self.gridLayout.addWidget(self.labelServerID, 1, 0, 1, 1)

        self.lineEditServerID = QLineEdit(self.layoutWidget)
        self.lineEditServerID.setObjectName(u"lineEditServerID")

        self.gridLayout.addWidget(self.lineEditServerID, 1, 1, 1, 1)

        self.labelServerSubNet = QLabel(self.layoutWidget)
        self.labelServerSubNet.setObjectName(u"labelServerSubNet")

        self.gridLayout.addWidget(self.labelServerSubNet, 1, 2, 1, 1)

        self.lineEditServerSubnet = QLineEdit(self.layoutWidget)
        self.lineEditServerSubnet.setObjectName(u"lineEditServerSubnet")

        self.gridLayout.addWidget(self.lineEditServerSubnet, 1, 3, 1, 1)

        self.labelCustomParam = QLabel(self.layoutWidget)
        self.labelCustomParam.setObjectName(u"labelCustomParam")

        self.gridLayout.addWidget(self.labelCustomParam, 2, 0, 1, 1)

        self.lineEditCustomParam = QLineEdit(self.layoutWidget)
        self.lineEditCustomParam.setObjectName(u"lineEditCustomParam")

        self.gridLayout.addWidget(self.lineEditCustomParam, 2, 1, 1, 3)


        self.verticalLayoutNetSetting.addWidget(self.groupBoxSetting)

        self.verticalLayoutWidget_3 = QWidget(self.centralwidget)
        self.verticalLayoutWidget_3.setObjectName(u"verticalLayoutWidget_3")
        self.verticalLayoutWidget_3.setGeometry(QRect(10, 300, 581, 411))
        self.verticalLayoutLogging = QVBoxLayout(self.verticalLayoutWidget_3)
        self.verticalLayoutLogging.setObjectName(u"verticalLayoutLogging")
        self.verticalLayoutLogging.setContentsMargins(0, 0, 0, 0)
        self.groupBoxLogging = QGroupBox(self.verticalLayoutWidget_3)
        self.groupBoxLogging.setObjectName(u"groupBoxLogging")
        self.plainTextEditLogging = QPlainTextEdit(self.groupBoxLogging)
        self.plainTextEditLogging.setObjectName(u"plainTextEditLogging")
        self.plainTextEditLogging.setGeometry(QRect(10, 30, 561, 371))
        self.plainTextEditLogging.setAutoFillBackground(True)
        self.plainTextEditLogging.setReadOnly(True)

        self.verticalLayoutLogging.addWidget(self.groupBoxLogging)

        self.verticalLayoutWidget_2 = QWidget(self.centralwidget)
        self.verticalLayoutWidget_2.setObjectName(u"verticalLayoutWidget_2")
        self.verticalLayoutWidget_2.setGeometry(QRect(10, 160, 581, 170))
        self.verticalLayoutSystemSetting = QVBoxLayout(self.verticalLayoutWidget_2)
        self.verticalLayoutSystemSetting.setObjectName(u"verticalLayoutSystemSetting")
        self.verticalLayoutSystemSetting.setContentsMargins(0, 0, 0, 0)
        self.groupBoxSystem = QGroupBox(self.verticalLayoutWidget_2)
        self.groupBoxSystem.setObjectName(u"groupBoxSystem")
        self.commandLinkButtonStart = QCommandLinkButton(self.groupBoxSystem)
        self.commandLinkButtonStart.setObjectName(u"commandLinkButtonStart")
        self.commandLinkButtonStart.setGeometry(QRect(270, 20, 91, 40))
        self.commandLinkButtonMonitor = QCommandLinkButton(self.groupBoxSystem)
        self.commandLinkButtonMonitor.setObjectName(u"commandLinkButtonMonitor")
        self.commandLinkButtonMonitor.setGeometry(QRect(270, 60, 181, 40))
        self.checkBoxAutoStart = QCheckBox(self.groupBoxSystem)
        self.checkBoxAutoStart.setObjectName(u"checkBoxAutoStart")
        self.checkBoxAutoStart.setGeometry(QRect(20, 40, 191, 19))
        self.checkBoxTray = QCheckBox(self.groupBoxSystem)
        self.checkBoxTray.setObjectName(u"checkBoxTray")
        self.checkBoxTray.setGeometry(QRect(20, 80, 191, 19))

        self.verticalLayoutSystemSetting.addWidget(self.groupBoxSystem)

        self.labelHappynVersion = QLabel(self.centralwidget)
        self.labelHappynVersion.setObjectName(u"labelHappynVersion")
        self.labelHappynVersion.setGeometry(QRect(30, 746, 161, 21))
        self.labelHappynCopyright = QLabel(self.centralwidget)
        self.labelHappynCopyright.setObjectName(u"labelHappynCopyright")
        self.labelHappynCopyright.setGeometry(QRect(180, 746, 191, 20))
        self.pushButtonExit = QPushButton(self.centralwidget)
        self.pushButtonExit.setObjectName(u"pushButtonExit")
        self.pushButtonExit.setGeometry(QRect(460, 739, 93, 30))

        QWidget.setTabOrder(self.lineServerPort, self.lineEditServerID)
        QWidget.setTabOrder(self.lineEditServerID, self.lineEditServerSubnet)
        QWidget.setTabOrder(self.lineEditServerSubnet, self.lineEditCustomParam)
        QWidget.setTabOrder(self.lineEditCustomParam, self.checkBoxAutoStart)
        QWidget.setTabOrder(self.checkBoxAutoStart, self.checkBoxTray)
        QWidget.setTabOrder(self.checkBoxTray, self.commandLinkButtonStart)
        QWidget.setTabOrder(self.commandLinkButtonStart, self.commandLinkButtonMonitor)
        QWidget.setTabOrder(self.commandLinkButtonMonitor, self.plainTextEditLogging)

        self.retranslateUi(HappynServerWindow)

        QMetaObject.connectSlotsByName(HappynServerWindow)
    # setupUi

    def retranslateUi(self, HappynServerWindow):
        HappynServerWindow.setWindowTitle(QCoreApplication.translate("HappynServerWindow", u"HappynServer", None))
        self.groupBoxSetting.setTitle(QCoreApplication.translate("HappynServerWindow", u"\u7f51\u7edc\u8bbe\u7f6e", None))
        self.labelServerPort.setText(QCoreApplication.translate("HappynServerWindow", u"\u76d1\u542c\u7aef\u53e3:", None))
        self.lineServerPort.setText(QCoreApplication.translate("HappynServerWindow", u"7654", None))
        self.labelServerID.setText(QCoreApplication.translate("HappynServerWindow", u"\u670d\u52a1ID:", None))
        self.lineEditServerID.setText(QCoreApplication.translate("HappynServerWindow", u"happyn001", None))
        self.labelServerSubNet.setText(QCoreApplication.translate("HappynServerWindow", u"\u5b50\u7f51\u8bbe\u5b9a:", None))
        self.lineEditServerSubnet.setText(QCoreApplication.translate("HappynServerWindow", u"192.168.100.0/24", None))
        self.labelCustomParam.setText(QCoreApplication.translate("HappynServerWindow", u"\u81ea\u5b9a\u4e49\u53c2\u6570:", None))
        self.groupBoxLogging.setTitle(QCoreApplication.translate("HappynServerWindow", u"\u65e5\u5fd7", None))
        self.groupBoxSystem.setTitle(QCoreApplication.translate("HappynServerWindow", u"\u670d\u52a1\u63a7\u5236", None))
        self.commandLinkButtonStart.setText(QCoreApplication.translate("HappynServerWindow", u"\u542f\u52a8", None))
        self.commandLinkButtonMonitor.setText(QCoreApplication.translate("HappynServerWindow", u"\u67e5\u770b\u5728\u7ebf\u8bbe\u5907", None))
        self.checkBoxAutoStart.setText(QCoreApplication.translate("HappynServerWindow", u"\u5f00\u673a\u81ea\u542f\u52a8", None))
        self.checkBoxTray.setText(QCoreApplication.translate("HappynServerWindow", u"\u6700\u5c0f\u5316\u5230\u6258\u76d8", None))
        self.labelHappynVersion.setText(QCoreApplication.translate("HappynServerWindow", u"HappynServer 1.0", None))
        self.labelHappynCopyright.setText(QCoreApplication.translate("HappynServerWindow", u"Powered by happyn.net", None))
        self.pushButtonExit.setText(QCoreApplication.translate("HappynServerWindow", u"\u9000\u51fa", None))
    # retranslateUi

