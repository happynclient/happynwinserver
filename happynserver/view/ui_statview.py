import time
from PySide2 import QtCore, QtWidgets, QtGui
from PySide2.QtGui import QFont
from PySide2.QtWidgets import QApplication
from ..controller.server import HPYServerManager
from ..model.config import HPYConfigManager


class UI_StatWindow(QtWidgets.QWidget):
    def __init__(self):
        super(UI_StatWindow, self).__init__()

        self.scale_font = QFont()
        self.scale_font.setPointSize(int(11 * QApplication.desktop().logicalDpiX() / 96.0))
        self.setFont(self.scale_font)

        self.config_manager = HPYConfigManager()
        manager_port = self.config_manager.extract_manager_port()
        self.server_manager = HPYServerManager(server_port=manager_port)

        self.clientModel = QtCore.QSortFilterProxyModel()
        self.clientModel.setDynamicSortFilter(True)
        # default set filter all key columns
        self.clientModel.setFilterKeyColumn(-1)

        self.serverGroupBox = QtWidgets.QGroupBox("happyn网络设备列表")
        self.clientGroupBox = QtWidgets.QGroupBox("happyn联网设备统计")

        self.serverView = QtWidgets.QTreeView()
        self.serverView.setRootIsDecorated(False)
        self.serverView.setAlternatingRowColors(True)

        self.clientView = QtWidgets.QTreeView()
        self.clientView.setRootIsDecorated(False)
        self.clientView.setAlternatingRowColors(True)
        self.clientView.setModel(self.clientModel)
        self.clientView.setSortingEnabled(True)

        self.sortCaseSensitivityCheckBox = QtWidgets.QCheckBox("Case sensitive sorting")
        self.filterCaseSensitivityCheckBox = QtWidgets.QCheckBox("Case sensitive filter")

        self.filterPatternLineEdit = QtWidgets.QLineEdit()
        self.filterPatternLabel = QtWidgets.QLabel("&搜索:")
        self.filterPatternLabel.setBuddy(self.filterPatternLineEdit)

        self.filterSyntaxComboBox = QtWidgets.QComboBox()
        self.filterSyntaxComboBox.addItem("Regular expression",
                QtCore.QRegExp.RegExp)
        self.filterSyntaxComboBox.addItem("Wildcard",
                QtCore.QRegExp.Wildcard)
        self.filterSyntaxComboBox.addItem("Fixed string",
                QtCore.QRegExp.FixedString)
        self.filterSyntaxLabel = QtWidgets.QLabel("Filter &syntax:")
        self.filterSyntaxLabel.setBuddy(self.filterSyntaxComboBox)

        self.filterColumnComboBox = QtWidgets.QComboBox()
        self.filterColumnComboBox.addItem("Subject")
        self.filterColumnComboBox.addItem("Sender")
        self.filterColumnComboBox.addItem("Date")
        self.filterColumnLabel = QtWidgets.QLabel("Filter &column:")
        self.filterColumnLabel.setBuddy(self.filterColumnComboBox)

        self.filterPatternLineEdit.textChanged.connect(self.filterRegExpChanged)
        self.filterSyntaxComboBox.currentIndexChanged.connect(self.filterRegExpChanged)
        self.filterColumnComboBox.currentIndexChanged.connect(self.filterColumnChanged)
        self.filterCaseSensitivityCheckBox.toggled.connect(self.filterRegExpChanged)
        self.sortCaseSensitivityCheckBox.toggled.connect(self.sortChanged)

        sourceLayout = QtWidgets.QHBoxLayout()
        sourceLayout.addWidget(self.serverView)
        self.serverGroupBox.setLayout(sourceLayout)

        proxyLayout = QtWidgets.QGridLayout()
        proxyLayout.addWidget(self.clientView, 0, 0, 1, 3)
        proxyLayout.addWidget(self.filterPatternLabel, 1, 0)
        proxyLayout.addWidget(self.filterPatternLineEdit, 1, 1, 1, 2)
        # proxyLayout.addWidget(self.filterColumnLabel, 3, 0)
        # proxyLayout.addWidget(self.filterColumnComboBox, 3, 1, 1, 2)
        self.clientGroupBox.setLayout(proxyLayout)

        self.updateTimer = QtCore.QTimer()
        self.updateTimer.timeout.connect(self.updateClientModel)

        mainLayout = QtWidgets.QVBoxLayout()
        #mainLayout.addWidget(self.serverGroupBox)
        mainLayout.addWidget(self.clientGroupBox)
        self.setLayout(mainLayout)

        icon = QtGui.QIcon()
        icon.addFile(u":/icons/icon144.png", QtCore.QSize(),
                        QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.setWindowIcon(icon)

        self.setWindowTitle("HappyServer Device Monitor")
        self.resize(900, 450)

        self.clientView.sortByColumn(1, QtCore.Qt.AscendingOrder)
        self.filterColumnComboBox.setCurrentIndex(0)

        self.filterPatternLineEdit.setText("")
        self.filterCaseSensitivityCheckBox.setChecked(False)
        self.sortCaseSensitivityCheckBox.setChecked(False)

    def closeEvent(self, event):
        # 在窗口关闭时停止定时器并释放资源
        self.updateTimer.stop()
        self.clientModel.setSourceModel(None)  # 释放模型

        # 调用父类的 closeEvent
        event.accept()

    def showEvent(self, event):
        # 启动定时器
        self.updateTimer.start(2000)

        super(UI_StatWindow, self).showEvent(event)  # 调用父类的 showEvent

    def updateClientModel(self):
        model = self.updateDeviceStatModel()
        self.clientModel.setSourceModel(model)
        self.clientView.header().resizeSection(0, 100)
        self.clientView.header().resizeSection(1, 80)
        self.clientView.header().resizeSection(2, 150)
        self.clientView.header().resizeSection(3, 150)
        self.clientView.header().resizeSection(4, 180)
        #self.clientView.setColumnWidth(0, 200)
        #self.clientView.resizeColumnToContents(0)

    def updateServerModel(self):
        model = self.updateDeviceStatModel()
        self.serverView.setModel(model)

    def filterRegExpChanged(self):
        syntax_nr = self.filterSyntaxComboBox.itemData(self.filterSyntaxComboBox.currentIndex())
        syntax = QtCore.QRegExp.PatternSyntax(syntax_nr)

        if self.filterCaseSensitivityCheckBox.isChecked():
            caseSensitivity = QtCore.Qt.CaseSensitive
        else:
            caseSensitivity = QtCore.Qt.CaseInsensitive

        regExp = QtCore.QRegExp(self.filterPatternLineEdit.text(),
                caseSensitivity, syntax)
        self.clientModel.setFilterRegExp(regExp)

    def filterColumnChanged(self):
        self.clientModel.setFilterKeyColumn(self.filterColumnComboBox.currentIndex())

    def sortChanged(self):
        if self.sortCaseSensitivityCheckBox.isChecked():
            caseSensitivity = QtCore.Qt.CaseSensitive
        else:
            caseSensitivity = QtCore.Qt.CaseInsensitive

        self.clientModel.setSortCaseSensitivity(caseSensitivity)

    def addDevice(self, model, community, name, mac, ip, sockaddr, uptime):
        model.insertRow(0)
        model.setData(model.index(0, 0), community)
        model.setData(model.index(0, 1), name)
        model.setData(model.index(0, 2), mac)
        model.setData(model.index(0, 3), ip)
        model.setData(model.index(0, 4), sockaddr)
        model.setData(model.index(0, 5), uptime)

    def updateDeviceStatModel(self):
        model = QtGui.QStandardItemModel(0, 6, self)

        model.setHeaderData(0, QtCore.Qt.Horizontal, "网络服务ID")
        model.setHeaderData(1, QtCore.Qt.Horizontal, "设备名称")
        model.setHeaderData(2, QtCore.Qt.Horizontal, "happyn mac地址")
        model.setHeaderData(3, QtCore.Qt.Horizontal, "happyn 内网ip")
        model.setHeaderData(4, QtCore.Qt.Horizontal, "外网通信ip:port")
        model.setHeaderData(5, QtCore.Qt.Horizontal, "最近活动时间")

        devices = self.server_manager.get_edges()
        for device in devices:
            self.addDevice(model, device['community'], device['desc'], device['macaddr'],
                             device['ip4addr'], device['sockaddr'],
                             QtCore.QDateTime.fromMSecsSinceEpoch(device['last_seen']*1000).toString('yyyy-MM-dd hh:mm:ss'))
                      #QtCore.QDateTime(QtCore.QDate(2006, 12, 22), QtCore.QTime(9, 44)))

        return model