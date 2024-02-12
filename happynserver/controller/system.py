import os
import sys
import ctypes
from PySide2.QtWidgets import QApplication, QMessageBox
from PySide2.QtCore import QCoreApplication
import winreg as reg


def add_to_startup(file_path=""):
    # 判断是否有管理员权限，并获取
    if not ctypes.windll.shell32.IsUserAnAdmin():
        QMessageBox.warning(None, '权限不足', '请使用管理员权限运行该程序以修改注册表.')
        return False

    # 如果没有提供一个路径，就用当前执行的文件路径
    if file_path == "":
        file_path = os.path.dirname(os.path.realpath(__file__))
        file_path = os.path.join(file_path, QCoreApplication.applicationName())

    # 注册表项名
    key = r"Software\Microsoft\Windows\CurrentVersion\Run"

    # 注册表操作
    try:
        # 连接注册表并写入键值
        registry_key = reg.OpenKey(reg.HKEY_CURRENT_USER, key, 0,
                                   reg.KEY_WRITE)
        reg.SetValueEx(registry_key, QCoreApplication.applicationName(), 0,
                       reg.REG_SZ, file_path)
        reg.CloseKey(registry_key)
        return True
    except WindowsError:
        return False


def remove_from_startup():
    # 检查权限
    if not ctypes.windll.shell32.IsUserAnAdmin():
        print("请使用管理员权限运行该程序以修改注册表.")
        return False

    # 注册表中负责开机自启的键的路径
    key_path = r"Software\Microsoft\Windows\CurrentVersion\Run"

    try:
        # 打开键
        registry_key = reg.OpenKey(reg.HKEY_CURRENT_USER, key_path, 0, reg.KEY_WRITE)
        # 删除值
        reg.DeleteValue(registry_key, QCoreApplication.applicationName())
        # 关闭键
        reg.CloseKey(registry_key)
        print(f"成功从开机自启动中移除{QCoreApplication.applicationName()}")
        return True
    except WindowsError:
        print("移除开机自启动失败")
        return False

# 使用以下方式在您的主应用程序中调用此函数:
if __name__ == "__main__":
    app = QApplication(sys.argv)
    add_to_startup()
    # ... 创建窗口等
    sys.exit(app.exec_())