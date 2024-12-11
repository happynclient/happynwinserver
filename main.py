import re
import os
import sys
import threading
import time
from win32 import win32gui
from PySide2.QtWidgets import QApplication, QFrame, QMessageBox, QFileDialog, QCheckBox
from PySide2.QtCore import QEvent, QObject, Signal, Slot
from PySide2 import QtCore

from happynserver.view.ui_trayicon import UITrayIcon
from happynserver.view.ui_main_window import Ui_HappynServerWindow
from happynserver.view.ui_statview import UI_StatWindow
from happynserver.model.config import HPYConfigManager
from happynserver.controller.service import ServiceManager
from happynserver.controller.server import HPYServerManager
from happynserver.controller.system import add_to_startup, remove_from_startup
import platform

def windowEnumerationHandler(hwnd, top_windows):
    top_windows.append((hwnd, win32gui.GetWindowText(hwnd)))

# 定义一个用于通信的类
class WorkerSignals(QObject):
    # 定义一个信号，没有参数
    update_log = Signal()

class HappynetUIMainWindow(QFrame, Ui_HappynServerWindow):
    def __init__(self):
        super(HappynetUIMainWindow, self).__init__()

        self.working_dir = self.get_current_working_directory()
        self.config_manager = HPYConfigManager()
        self.service_manager = ServiceManager("HappynServer", self.working_dir)

        # 将UI界面布局到Demo上；
        self.setupUi(self)

        # 创建托盘图标实例
        self.tray_icon = UITrayIcon(self)
        # self.tray_icon.show()

        # 连接按钮的clicked信号到窗口的close方法
        self.pushButtonExit.clicked.connect(self.close)

        # 创建信号实例
        self.worker_signals = WorkerSignals()
        self.worker_signals.update_log.connect(self.refresh_log_window)

    def setupUi(self, HappynServerWindow):
        # 首先调用基类的setupUi来继承原有的UI设置
        super().setupUi(HappynServerWindow)

        # 设置默认配置
        if not self.config_manager.load_config():
            # 使用默认配置初始化或更新注册表
            default_config = {
                "ServerPort": 7654,
                "ServerNetConf": "etc/happynserver.conf",
                "CustomParam": "",
                "IsAutoStart": 0,
                "IsMinToTray": 1
            }
            self.config_manager.update(default_config)
        self.load_gui_from_config()

        self.statwindow = None

        self.commandLinkButtonMonitor.setEnabled(False)  # 初始状态设置为不可点击
        self.commandLinkButtonStart.clicked.connect(self.toggle_service)
        self.commandLinkButtonMonitor.clicked.connect(self.openMonitorWindow)
        self.pushButtonFileSelect.clicked.connect(self.selectFile)
        self.checkBoxTray.stateChanged.connect(self.onCheckBoxTrayStateChanged)
        self.checkBoxAutoStart.stateChanged.connect(self.onCheckBoxAutoStartStateChanged)

        self.start_monitoring_service()

    def selectFile(self):
        filename, _ = QFileDialog.getOpenFileName()
        self.lineEditServerNetConf.setText(filename)

    def get_current_working_directory(self):
        base_path = os.path.realpath(os.path.dirname(sys.argv[0]))
        # QMessageBox.warning(self, "路径", base_path, QMessageBox.Ok)
        return base_path

    def toggle_service(self):
        if self.service_manager.is_service_exist() and self.service_manager.get_service_status():
            self.stop_service()
        else:
            self.start_service()

    def start_service(self):
        if self.save_gui_to_config():
            command_line = self.config_manager.generate_command_line()
            self.service_manager.upsert_service(command_line)
            self.service_manager.start_service()

    def stop_service(self):
        port = self.config_manager.extract_manager_port()
        manager = HPYServerManager(server_port=port)
        manager.stop()
        time.sleep(1)
        self.worker_signals.update_log.emit()
        self.service_manager.stop_service()

    def onCheckBoxTrayStateChanged(self, state):
        # 根据复选框的状态执行操作
        if state == QtCore.Qt.Checked:
            print("Tray CheckBox is checked")
            self.config_manager.set("IsMinToTray", 1)
        else:
            print("CheckBox is unchecked")
            self.config_manager.set("IsMinToTray", 0)
        self.config_manager.save_config()

    def onCheckBoxAutoStartStateChanged(self, state):
        # 根据复选框的状态执行操作
        if state == QtCore.Qt.Checked:
            print("AutoStart CheckBox is checked")
            self.config_manager.set("IsAutoStart", 1)
            self.service_manager.set_service_auto_start()
            add_to_startup()
        else:
            print("AutoStart is unchecked")
            self.config_manager.set("IsAutoStart", 0)
            self.service_manager.unset_service_auto_start()
            remove_from_startup()
        self.config_manager.save_config()

    def openMonitorWindow(self):
        if not self.statwindow:  # 检查是否已经打开了统计窗口
            self.statwindow = UI_StatWindow()  # 创建一个属性来保存它
        self.statwindow.show()  # 显示窗口

    # 在这里增加刷新日志窗口的逻辑
    @Slot()
    def refresh_log_window(self):
        # 这里编写刷新日志窗口的代码
        # 例如，self.textEditLog.setPlainText(log_content)
        logs = self.service_manager.get_logs()
        self.plainTextEditLogging.setPlainText(logs)
        # 滚动到底部
        scrollbar = self.plainTextEditLogging.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())

    def start_monitoring_service(self):
        # 创建并启动监控线程
        thread = threading.Thread(target=self.monitor_service_status)
        thread.daemon = True
        thread.start()

    def monitor_service_status(self):
        while True:
            # 检测服务状态
            if self.service_manager.is_service_exist():
                if self.service_manager.get_service_status():
                    self.commandLinkButtonStart.setText("停止")
                    self.commandLinkButtonMonitor.setEnabled(True)
                    # 如果服务正在运行，发射信号更新日志窗口
                    self.worker_signals.update_log.emit()
                else:
                    self.commandLinkButtonStart.setText("启动")
                    self.commandLinkButtonMonitor.setEnabled(False)
            else:
                self.commandLinkButtonStart.setText("启动")
                self.commandLinkButtonMonitor.setEnabled(False)
            time.sleep(1)  # 每隔1秒检查一次服务状态

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

        self.config_manager.set('ServerNetConf', self.lineEditServerNetConf.text())
        self.config_manager.set('CustomParam', self.lineEditCustomParam.text())

        self.config_manager.set('IsMinToTray', self.checkBoxTray.isChecked())
        self.config_manager.set('IsAutoStart', self.checkBoxAutoStart.isChecked())
        return True

    def load_gui_from_config(self):
        self.lineServerPort.setText(str(self.config_manager.get('ServerPort')))
        self.lineEditServerNetConf.setText(self.config_manager.get('ServerNetConf'))
        self.lineEditCustomParam.setText(self.config_manager.get('CustomParam'))

        self.checkBoxTray.setChecked(self.config_manager.get('IsMinToTray'))
        self.checkBoxAutoStart.setChecked(self.config_manager.get('IsAutoStart'))

    def changeEvent(self, event):
        if event.type() == QEvent.WindowStateChange:
            if self.isMinimized() and self.config_manager.get("IsMinToTray"):
                self.hide()  # 在窗口最小化时隐藏窗口
                self.tray_icon.show()  # 显示托盘图标
            else:
                super().changeEvent(event)  # 处理其他状态变化

    def closeEvent(self, event):
        if self.service_manager.is_service_exist() and self.service_manager.get_service_status():
            # 弹出确认对话框
            reply = QMessageBox.question(self, '确认退出', '关闭窗口会退出当前服务，确定退出吗？',
                                         QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

            if reply == QMessageBox.Yes:
                self.stop_service()
                event.accept()  # 用户确认退出
            else:
                event.ignore()  # 用户取消退出，忽略关闭事件


if __name__ == "__main__":
    top_windows = []
    win32gui.EnumWindows(windowEnumerationHandler, top_windows)
    for i in top_windows:
        if "HappynServer" in i[1]:  # CHANGE PROGRAM TO THE NAME OF YOUR WINDOW
            win32gui.ShowWindow(i[0], 5)
            win32gui.SetForegroundWindow(i[0])
            sys.exit()

    QtCore.QCoreApplication.setAttribute(QtCore.Qt.ApplicationAttribute.AA_EnableHighDpiScaling)
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.ApplicationAttribute.AA_UseHighDpiPixmaps)
    app = QApplication(sys.argv)

    mainWindow = HappynetUIMainWindow()
    mainWindow.tray_icon = UITrayIcon(mainWindow)
    mainWindow.show()
    sys.exit(app.exec_())
