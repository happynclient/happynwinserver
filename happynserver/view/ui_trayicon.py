from PySide2.QtWidgets import QSystemTrayIcon, QMenu
from PySide2.QtGui import QIcon

class UITrayIcon(QSystemTrayIcon):
    def __init__(self, parent=None):
        super(UITrayIcon, self).__init__(parent)
        self.setIcon(QIcon("res/happynserver.ico"))  # 设置托盘图标

        # 创建托盘的右键菜单
        self.trayMenu = QMenu(parent)
        exit_action = self.trayMenu.addAction('退出')
        exit_action.triggered.connect(parent.close)  # 假设父窗口有close方法

        self.setContextMenu(self.trayMenu)
        self.activated.connect(self.on_activated)

    def on_activated(self, reason):
        if reason in [QSystemTrayIcon.Trigger, QSystemTrayIcon.DoubleClick]:
            parent = self.parent()
            if parent.isMinimized():
                parent.showNormal()  # 如果窗口最小化了，则恢复
                parent.activateWindow()
                self.hide()
            else:
                parent.activateWindow()  # 否则，激活窗口
