import sys

from happynserver.view.ui_trayicon import UITrayIcon
from happynserver.view.ui_main_window import Ui_HappynServerWindow
from PySide2.QtWidgets import QApplication, QFrame
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

    def changeEvent(self, event):
        if event.type() == QEvent.WindowStateChange:
            if self.isMinimized():
                self.hide()  # 在窗口最小化时隐藏窗口
                self.tray_icon.show()  # 显示托盘图标
            else:
                super().changeEvent(event)  # 处理其他状态变化


if __name__ == "__main__":
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.ApplicationAttribute.AA_EnableHighDpiScaling)
    app = QApplication(sys.argv)
    mainWindow = HappynetUIMainWindow()
    mainWindow.tray_icon = UITrayIcon(mainWindow)
    mainWindow.show()
    sys.exit(app.exec_())
