import re
import os
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

        self.working_dir = self.get_current_working_directory()
        self.config_manager = HPYConfigManager()
        self.service_manager = ServiceManager("HappynServer")

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
        if not self.config_manager.load_config():
            # 使用默认配置初始化或更新注册表
            default_config = {
                "ServerPort": 7644,
                "ServerID": "happyn001",
                "ServerSubnet": "192.168.100.0/24",
                "CustomParam": "",
                "IsAutoStart": 1,
                "IsMinToTray": 1
            }
            self.config_manager.update(default_config)
        self.load_gui_from_config()

        self.commandLinkButtonMonitor.setEnabled(False)  # 初始状态设置为不可点击
        self.commandLinkButtonStart.clicked.connect(self.toggle_service)
        self.commandLinkButtonMonitor.clicked.connect(self.openMonitorWindow)

    def get_current_working_directory(self):
        # 获取当前文件的绝对路径
        abs_file_path = os.path.abspath(__file__)
        # 获取当前文件所在的目录
        directory = os.path.dirname(abs_file_path)
        return directory

    def toggle_service(self):
        if self.service_manager.get_service_status():
            self.stop_service()
        else:
            self.start_service()

    def start_service(self):
        if self.save_gui_to_config():
            command_line = self.config_manager.generate_command_line(self.working_dir)
            self.service_manager.upsert_service(command_line)  # 假设这是启动服务的方法
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
        try:
            port = int(self.lineServerPort.text())
            if 1 <= port <= 65535:
                self.config_manager.set('ServerPort', port)
            else:
                raise ValueError
        except ValueError:
            QMessageBox.warning(self, "无效端口", "端口号必须是1到65535之间的整数。", QMessageBox.Ok)
            self.lineServerPort.setFocus()
            return False


        # 正则表达式用于匹配IPv4地址/掩码格式
        subnet_pattern = re.compile(r'^(\d{1,3}\.){3}\d{1,3}\/\d{1,2}$')
        match = subnet_pattern.match(self.lineEditServerSubnet.text())

        if match:
            parts = self.lineEditServerSubnet.text().split('/')
            ip_parts = parts[0].split('.')
            mask = int(parts[1])

            if all(0 <= int(part) <= 255 for part in ip_parts) and 0 <= mask <= 32:
                self.config_manager.set('ServerSubnet', self.lineEditServerSubnet.text())
            else:
                QMessageBox.warning(self, "无效子网格式", "子网格式不正确，请输入正确的子网，如192.168.100.0/24。",
                                    QMessageBox.Ok)
                self.lineEditServerSubnet.setFocus()
                return False
        else:
            QMessageBox.warning(self, "无效子网格式", "子网格式不正确，请输入正确的子网，如192.168.100.0/24。",
                                QMessageBox.Ok)
            self.lineEditServerSubnet.setFocus()
            return False

        self.config_manager.set('ServerID', self.lineEditServerID.text())
        self.config_manager.set('CustomParam', self.lineEditCustomParam.text())

        self.config_manager.set('IsMinToTray', self.checkBoxTray.isChecked())
        self.config_manager.set('IsAutoStart', self.checkBoxAutoStart.isChecked())
        return True

    def load_gui_from_config(self):
        self.lineServerPort.setText(str(self.config_manager.get('ServerPort')))
        self.lineEditServerID.setText(self.config_manager.get('ServerID'))
        self.lineEditServerSubnet.setText(self.config_manager.get('ServerSubnet'))
        self.lineEditCustomParam.setText(self.config_manager.get('CustomParam'))

        self.checkBoxTray.setChecked(self.config_manager.get('IsMinToTray'))
        self.checkBoxAutoStart.setChecked(self.config_manager.get('IsAutoStart'))

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
