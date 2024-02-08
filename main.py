import sys

from happynserver.view.ui_trayicon import UITrayIcon
from happynserver.view.ui_main_window import Ui_HappynServerWindow
from PySide2.QtWidgets import QApplication, QFrame
from PySide2 import QtCore
import platform
from ctypes import windll

class HappynetUIMainWindow(QFrame, Ui_HappynServerWindow):
    def __init__(self):
        super(HappynetUIMainWindow, self).__init__()
        # 将UI界面布局到Demo上；
        self.setupUi(self)

    def changeEvent(self, event):
        if event.type() == 8:  # 8 表示窗口最小化事件
            self.hide_taskbar_button()

    def hide_taskbar_button(self):
        if platform.system() == 'Windows':
            hwnd = self.winId()
            windll.user32.ShowWindow(hwnd, 0x8)  # 0x8 表示SW_HIDE

if __name__ == "__main__":
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.ApplicationAttribute.AA_EnableHighDpiScaling)
    app = QApplication(sys.argv)
    main_window = HappynetUIMainWindow()
    tray_icon = UITrayIcon(app, main_window=main_window)
    tray_icon.show()
    tray_icon.on_show_main_window()
    sys.exit(app.exec_())
