import sys
from PySide2.QtWidgets import QApplication, QMenu, QAction, QSystemTrayIcon
from PySide2.QtGui import QIcon, QPixmap


class UITrayIcon(QSystemTrayIcon):
    def __init__(self, parent=None, main_window=None):
        super().__init__(parent)

        # 获取初始配置项
        self.is_tray = True
        self.is_started = False
        self.main_window = main_window
        self.main_window.windowIconChanged.connect(self.update_tray_icon)
        self.menu = QMenu()

        self.start_stop_action = QAction("Start/Stop", triggered=self.on_start_stop)
        self.menu.addAction(self.start_stop_action)
        self.settings_action = QAction("Settings", triggered=self.on_settings)
        self.menu.addAction(self.settings_action)
        self.show_main_window = QAction("Show Main Dialog", triggered=self.on_show_main_window)
        self.menu.addAction(self.show_main_window)
        self.about_action = QAction("About", triggered=self.on_about)
        self.menu.addAction(self.about_action)
        self.setContextMenu(self.menu)

        self.update_tray_icon()

    def update_tray_icon(self):
        if self.main_window.isMinimized() and self.is_started:
            self.setIcon(QIcon("res/happynet_start.ico"))
        elif self.main_window.isMinimized() and not self.is_started:
            self.setIcon(QIcon("res/happynet_stop.ico"))
        else:
            self.setIcon(QIcon())
            print("不要显示托盘")

    def on_show_main_window(self):
        # 处理点击 Show Main Dialog 菜单的逻辑
        print("Show Main Dialog 被点击")
        if not self.main_window.isVisible():  # 当主窗口不可见时
            self.main_window.showNormal()  # 显示主窗口
            self.main_window.activateWindow()  # 激活主窗口
        self.update_tray_icon()

    def on_start_stop(self):
        # 处理点击 Start/Stop 菜单的逻辑
        print("Start/Stop 被点击")
        self.is_started = not self.is_started
        self.update_tray_icon()

    def on_settings(self):
        # 处理点击 Settings 菜单的逻辑
        print("Settings 被点击")

    def on_about(self):
        # 处理点击 About 菜单的逻辑
        print("About 被点击")