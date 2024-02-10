import sys

from happynserver.view.ui_trayicon import UITrayIcon
from happynserver.view.ui_main_window import Ui_HappynServerWindow
from happynserver.model.config import HPYConfigManager
from happynserver.controller.service import ServiceManager
from PySide2.QtWidgets import QApplication, QFrame, QMessageBox
from PySide2.QtCore import QEvent
from PySide2 import QtCore
import platform
from ctypes import windll


class HappynetUIMainWindow(QFrame, Ui_HappynServerWindow):
    def __init__(self):
        super(HappynetUIMainWindow, self).__init__()

        self.config = {}
        self.config_manager = HPYConfigManager()
        self.service_manager = ServiceManager("MyService",
                                              "python my_service.py --port {port} --id {service_id}")

        # 将UI界面布局到Demo上；
        self.setupUi(self)

        # 创建托盘图标实例
        self.tray_icon = UITrayIcon(self)
        # self.tray_icon.show()

        # 连接按钮的clicked信号到窗口的close方法
        self.pushButtonExit.clicked.connect(self.close)


    def setupUi(self, HappynServerWindow):
        # 首先调用基类的setupUi来继承原有的UI设置
        super().setupUi(HappynServerWindow)

        # 设置默认配置
        self.config = self.config_manager.load_config()
        if not self.config:
            # 使用默认配置初始化或更新注册表
            config = {
                "ServerPort": 7644,
                "ServerID": "happyn001",
                "ServerSubnet": "192.168.100.0/24",
                "CustomParam": "",
                "IsAutoStart": 1,
                "IsMinToTray": 1
            }
            self.config_manager.update(config)
        self.load_gui_from_config()

        self.commandLinkButtonMonitor.setEnabled(False)  # 初始状态设置为不可点击
        self.commandLinkButtonStart.clicked.connect(self.toggle_service)
        self.commandLinkButtonMonitor.clicked.connect(self.openMonitorWindow)

    def toggle_service(self):
        if self.service_manager.get_service_status():
            self.stop_service()
        else:
            self.start_service()

    def start_service(self):
        self.save_gui_to_config()
        # service_manager.start_service()  # 假设这是启动服务的方法
        self.service_manager.start_service()
        self.commandLinkButtonStart.setText("停止")
        self.commandLinkButtonMonitor.setEnabled(True)


    def stop_service(self):
        # service_manager.stop_service()  # 假设这是停止服务的方法
        self.service_manager.stop_service()
        self.commandLinkButtonStart.setText("启动")
        self.commandLinkButtonMonitor.setEnabled(False)

    def openMonitorWindow(self):
        pass

    def save_gui_to_config(self):
        self.config['ServerPort'] = self.lineServerPort.text()
        self.config['ServerID'] = self.lineEditServerID.text()
        self.config['ServerSubnet'] = self.lineEditServerSubnet.text()
        self.config['CustomParam'] = self.lineEditCustomParam.text()

        self.config['IsMinToTray'] = self.checkBoxTray.isChecked()
        self.config['IsAutoStart'] = self.checkBoxAutoStart.isChecked()
        self.config_manager.update(self.config)

    def load_gui_from_config(self):
        self.lineServerPort.setText(str(self.config['ServerPort']))
        self.lineEditServerID.setText(self.config['ServerID'])
        self.lineEditServerSubnet.setText(self.config['ServerSubnet'])
        self.lineEditCustomParam.setText(self.config['CustomParam'])

        self.checkBoxTray.setChecked(self.config['IsMinToTray'])
        self.checkBoxAutoStart.setChecked(self.config['IsAutoStart'])

    def changeEvent(self, event):
        if event.type() == QEvent.WindowStateChange:
            if self.isMinimized():
                self.hide()  # 在窗口最小化时隐藏窗口
                self.tray_icon.show()  # 显示托盘图标
            else:
                super().changeEvent(event)  # 处理其他状态变化

    def closeEvent(self, event):
        if self.service_manager.get_service_status():
            # 弹出确认对话框
            reply = QMessageBox.question(self, '确认退出', '关闭窗口会退出当前服务，确定退出吗？',
                                         QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

            if reply == QMessageBox.Yes:
                event.accept()  # 用户确认退出
            else:
                event.ignore()  # 用户取消退出，忽略关闭事件


if __name__ == "__main__":
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.ApplicationAttribute.AA_EnableHighDpiScaling)
    app = QApplication(sys.argv)
    mainWindow = HappynetUIMainWindow()
    mainWindow.tray_icon = UITrayIcon(mainWindow)
    mainWindow.show()
    sys.exit(app.exec_())
