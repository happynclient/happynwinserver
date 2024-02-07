# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mainGUIAtkasy.ui'
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
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(HappynServerWindow.sizePolicy().hasHeightForWidth())
        HappynServerWindow.setSizePolicy(sizePolicy)
        HappynServerWindow.setMinimumSize(QSize(0, 0))
        HappynServerWindow.setMaximumSize(QSize(800, 800))
        icon = QIcon()
        icon.addFile(u":/icons/icon144.png", QSize(), QIcon.Normal, QIcon.Off)
        icon.addFile(u":/icons/icon144.png", QSize(), QIcon.Normal, QIcon.On)
        HappynServerWindow.setWindowIcon(icon)
        self.centralwidget = QWidget(HappynServerWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.buttonBox = QDialogButtonBox(self.centralwidget)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setGeometry(QRect(210, 720, 341, 32))
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)
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
        self.label = QLabel(self.layoutWidget)
        self.label.setObjectName(u"label")

        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)

        self.lineEdit = QLineEdit(self.layoutWidget)
        self.lineEdit.setObjectName(u"lineEdit")

        self.gridLayout.addWidget(self.lineEdit, 0, 1, 1, 1)

        self.label_2 = QLabel(self.layoutWidget)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)

        self.lineEdit_2 = QLineEdit(self.layoutWidget)
        self.lineEdit_2.setObjectName(u"lineEdit_2")

        self.gridLayout.addWidget(self.lineEdit_2, 1, 1, 1, 1)

        self.label_3 = QLabel(self.layoutWidget)
        self.label_3.setObjectName(u"label_3")

        self.gridLayout.addWidget(self.label_3, 1, 2, 1, 1)

        self.lineEdit_3 = QLineEdit(self.layoutWidget)
        self.lineEdit_3.setObjectName(u"lineEdit_3")

        self.gridLayout.addWidget(self.lineEdit_3, 1, 3, 1, 1)

        self.label_7 = QLabel(self.layoutWidget)
        self.label_7.setObjectName(u"label_7")

        self.gridLayout.addWidget(self.label_7, 2, 0, 1, 1)

        self.lineEdit_4 = QLineEdit(self.layoutWidget)
        self.lineEdit_4.setObjectName(u"lineEdit_4")

        self.gridLayout.addWidget(self.lineEdit_4, 2, 1, 1, 3)


        self.verticalLayoutNetSetting.addWidget(self.groupBoxSetting)

        self.verticalLayoutWidget_3 = QWidget(self.centralwidget)
        self.verticalLayoutWidget_3.setObjectName(u"verticalLayoutWidget_3")
        self.verticalLayoutWidget_3.setGeometry(QRect(10, 300, 581, 411))
        self.verticalLayoutLogging = QVBoxLayout(self.verticalLayoutWidget_3)
        self.verticalLayoutLogging.setObjectName(u"verticalLayoutLogging")
        self.verticalLayoutLogging.setContentsMargins(0, 0, 0, 0)
        self.groupBox_2 = QGroupBox(self.verticalLayoutWidget_3)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.plainTextEdit = QPlainTextEdit(self.groupBox_2)
        self.plainTextEdit.setObjectName(u"plainTextEdit")
        self.plainTextEdit.setGeometry(QRect(10, 30, 561, 371))
        self.plainTextEdit.setAutoFillBackground(True)
        self.plainTextEdit.setReadOnly(True)

        self.verticalLayoutLogging.addWidget(self.groupBox_2)

        self.verticalLayoutWidget_2 = QWidget(self.centralwidget)
        self.verticalLayoutWidget_2.setObjectName(u"verticalLayoutWidget_2")
        self.verticalLayoutWidget_2.setGeometry(QRect(10, 160, 581, 170))
        self.verticalLayoutSystemSetting = QVBoxLayout(self.verticalLayoutWidget_2)
        self.verticalLayoutSystemSetting.setObjectName(u"verticalLayoutSystemSetting")
        self.verticalLayoutSystemSetting.setContentsMargins(0, 0, 0, 0)
        self.groupBox = QGroupBox(self.verticalLayoutWidget_2)
        self.groupBox.setObjectName(u"groupBox")
        self.commandLinkButton = QCommandLinkButton(self.groupBox)
        self.commandLinkButton.setObjectName(u"commandLinkButton")
        self.commandLinkButton.setGeometry(QRect(270, 20, 91, 40))
        self.commandLinkButton_2 = QCommandLinkButton(self.groupBox)
        self.commandLinkButton_2.setObjectName(u"commandLinkButton_2")
        self.commandLinkButton_2.setGeometry(QRect(270, 60, 181, 40))
        self.checkBox = QCheckBox(self.groupBox)
        self.checkBox.setObjectName(u"checkBox")
        self.checkBox.setGeometry(QRect(20, 40, 191, 19))
        self.checkBox_2 = QCheckBox(self.groupBox)
        self.checkBox_2.setObjectName(u"checkBox_2")
        self.checkBox_2.setGeometry(QRect(20, 80, 191, 19))

        self.verticalLayoutSystemSetting.addWidget(self.groupBox)

        self.statusbar = QStatusBar(HappynServerWindow)
        self.menubar = QMenuBar(HappynServerWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 600, 26))

        QWidget.setTabOrder(self.lineEdit, self.lineEdit_2)
        QWidget.setTabOrder(self.lineEdit_2, self.lineEdit_3)
        QWidget.setTabOrder(self.lineEdit_3, self.lineEdit_4)
        QWidget.setTabOrder(self.lineEdit_4, self.checkBox)
        QWidget.setTabOrder(self.checkBox, self.checkBox_2)
        QWidget.setTabOrder(self.checkBox_2, self.commandLinkButton)
        QWidget.setTabOrder(self.commandLinkButton, self.commandLinkButton_2)
        QWidget.setTabOrder(self.commandLinkButton_2, self.plainTextEdit)

        self.retranslateUi(HappynServerWindow)

        QMetaObject.connectSlotsByName(HappynServerWindow)
    # setupUi

    def retranslateUi(self, HappynServerWindow):
        HappynServerWindow.setWindowTitle(QCoreApplication.translate("HappynServerWindow", u"HappynServer", None))
        self.groupBoxSetting.setTitle(QCoreApplication.translate("HappynServerWindow", u"\u8bbe\u7f6e", None))
        self.label.setText(QCoreApplication.translate("HappynServerWindow", u"\u76d1\u542c\u7aef\u53e3:", None))
        self.lineEdit.setText(QCoreApplication.translate("HappynServerWindow", u"7654", None))
        self.label_2.setText(QCoreApplication.translate("HappynServerWindow", u"\u670d\u52a1ID:", None))
        self.lineEdit_2.setText(QCoreApplication.translate("HappynServerWindow", u"happyn001", None))
        self.label_3.setText(QCoreApplication.translate("HappynServerWindow", u"\u5b50\u7f51\u8bbe\u5b9a:", None))
        self.lineEdit_3.setText(QCoreApplication.translate("HappynServerWindow", u"192.168.100.0/24", None))
        self.label_7.setText(QCoreApplication.translate("HappynServerWindow", u"\u81ea\u5b9a\u4e49\u53c2\u6570:", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("HappynServerWindow", u"\u65e5\u5fd7", None))
        self.groupBox.setTitle(QCoreApplication.translate("HappynServerWindow", u"\u670d\u52a1\u63a7\u5236", None))
        self.commandLinkButton.setText(QCoreApplication.translate("HappynServerWindow", u"\u542f\u52a8", None))
        self.commandLinkButton_2.setText(QCoreApplication.translate("HappynServerWindow", u"\u67e5\u770b\u5728\u7ebf\u8bbe\u5907", None))
        self.checkBox.setText(QCoreApplication.translate("HappynServerWindow", u"\u5f00\u673a\u81ea\u542f\u52a8", None))
        self.checkBox_2.setText(QCoreApplication.translate("HappynServerWindow", u"\u6700\u5c0f\u5316\u5230\u6258\u76d8", None))
    # retranslateUi

