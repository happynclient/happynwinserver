import sys

from happynserver.view.ui_trayicon import UITrayIcon
from happynserver.view.ui_main_window import Ui_HappynServerWindow
from happynserver.model.config import HPYConfigManager
from PySide2.QtWidgets import QApplication, QFrame, QMessageBox
from PySide2.QtCore import QEvent
from PySide2 import QtCore
import platform
from ctypes import windll


class HappynetUIMainWindow(QFrame, Ui_HappynServerWindow):
    def __init__(self):
        super(HappynetUIMainWindow, self).__init__()
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
        config_manager = HPYConfigManager()

        # 设置默认配置
        default_config = {
            "ServerPort": 7644,
            "ServerID": "happyn001",
            "ServerSubnet": "192.168.100.0/24",
            "CustomParam": "",
            "IsAutoStart": 1,
            "IsMinToTray": 1
        }
        # 使用默认配置初始化或更新注册表
        config_manager.update(default_config)

        self.lineServerPort.setText(str(default_config['ServerPort']))


    def changeEvent(self, event):
        if event.type() == QEvent.WindowStateChange:
            if self.isMinimized():
                self.hide()  # 在窗口最小化时隐藏窗口
                self.tray_icon.show()  # 显示托盘图标
            else:
                super().changeEvent(event)  # 处理其他状态变化

    def closeEvent(self, event):
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
