"""
# 示例用法
# 无论调用多少次ServiceManager，返回的都是同一个实例
service_manager1 = ServiceManager("MyService", "python my_service.py --port {port} --id {service_id}")
service_manager2 = ServiceManager("MyService", "python my_service.py --port {port} --id {service_id}")
assert service_manager1 is service_manager2  # 这将证明service_manager1和service_manager2是同一个实例
"""
import chardet
import subprocess
import os
import win32service
import win32serviceutil

HAPPYNSERVER_DESC = "HappynServer is a light VPN software which makes it "\
                    "easy to create virtual networks by passing intermediate firewalls. "\
                    "Powered by happyn.net"

class SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(SingletonMeta, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class ServiceManager(metaclass=SingletonMeta):
    def __init__(self, service_name, working_dir):
        self.service_name = service_name
        self.working_dir = working_dir
        self.log_file = f'{os.path.join(self.working_dir, self.service_name)}.log'
        self.service_status = 0

    # nssm install <servicename> <program> [<arguments>]
    # nssm set <servicename> Description "xxxx"
    # nssm set <servicename> AppStdout <logpath>
    def create_service(self, params):
        create_command = f'{os.path.join(self.working_dir, "utility", "happynssm.exe")} install {self.service_name} ' + \
                         f'{os.path.join(self.working_dir, "utility", "happynsupernode.exe")} "{params}"'
        print(create_command)
        subprocess.run(create_command, shell=True)

        setdesc_command = f'{os.path.join(self.working_dir, "utility", "happynssm.exe")}  set {self.service_name} ' + \
                          f'Description "{HAPPYNSERVER_DESC}"'
        print(setdesc_command)
        subprocess.run(setdesc_command, shell=True)

        setlog_command = f'{os.path.join(self.working_dir, "utility", "happynssm.exe")}  set {self.service_name} ' + \
                         f'AppStdout {self.log_file}'
        print(setlog_command)
        subprocess.run(setlog_command, shell=True)

    # nssm.exe set <servicename> AppParameters <arguments>
    def update_service(self, params):
        update_command = f'{os.path.join(self.working_dir, "utility", "happynssm.exe")} set {self.service_name} ' + \
                         f'AppParameters {os.path.join(self.working_dir, "utility", "happynsupernode.exe")} "{params}"'
        print(update_command)
        subprocess.run(update_command, shell=True)

    # nssm start <servicename>
    def start_service(self):
        start_command = f'{os.path.join(self.working_dir, "utility", "happynssm.exe")} start {self.service_name}'
        print(start_command)
        subprocess.run(start_command, shell=True)

    def stop_service(self):
        stop_command = f'{os.path.join(self.working_dir, "utility", "happynssm.exe")} stop {self.service_name}'
        print(stop_command)
        subprocess.run(stop_command, shell=True)

    #  nssm remove <servicename>
    def delete_service(self):
        if not self.is_service_exist():
            return
        if self.get_service_status():
            self.stop_service()
        delete_command = f'{os.path.join(self.working_dir, "utility", "happynssm.exe")} remove {self.service_name} confirm'
        print(delete_command)
        subprocess.run(delete_command, shell=True)

    # nssm set <servicename> Start SERVICE_AUTO_START
    def set_service_auto_start(self):
        auto_start_command = f'{os.path.join(self.working_dir, "utility", "happynssm.exe")} ' + \
                             f'set {self.service_name} Start SERVICE_AUTO_START'
        print(auto_start_command)
        subprocess.run(auto_start_command, shell=True)

    def unset_service_auto_start(self):
        unset_auto_start_command = f'{os.path.join(self.working_dir, "utility", "happynssm.exe")} ' + \
                             f'set {self.service_name} Start SERVICE_DEMAND_START'
        print(unset_auto_start_command)
        subprocess.run(unset_auto_start_command, shell=True)

    """Return: 1 running
               0 stopped
    """
    def get_service_status(self):
        try:
            # 打开服务控制管理器
            sch = win32service.OpenSCManager(None, None, win32service.SC_MANAGER_ALL_ACCESS)

            # 打开指定的服务
            svc = win32service.OpenService(sch, self.service_name, win32service.SC_MANAGER_ALL_ACCESS)

            # 查询服务状态
            status = win32service.QueryServiceStatusEx(svc)

            # 关闭服务和服务控制管理器的句柄
            win32service.CloseServiceHandle(svc)
            win32service.CloseServiceHandle(sch)

            # 检查服务状态
            if status['CurrentState'] == win32service.SERVICE_RUNNING:
                self.service_status = 1
            else:
                self.service_status = 0
        except Exception as e:
            print(f"Error: {e}")
            return "EXCEPTION"
        return self.service_status

    def is_service_exist(self):
        try:
            # 打开服务控制管理器
            sch = win32service.OpenSCManager(None, None, win32service.SC_MANAGER_ALL_ACCESS)

            # 打开指定的服务
            svc = win32service.OpenService(sch, self.service_name, win32service.SC_MANAGER_ALL_ACCESS)
            # 查询服务状态
            status = win32service.QueryServiceStatusEx(svc)

            # 关闭服务和服务控制管理器的句柄
            win32service.CloseServiceHandle(svc)
            win32service.CloseServiceHandle(sch)
        except Exception as e:
            print(f"Error: {e}")
            return False
        return True

    def upsert_service(self, params):
        if self.is_service_exist():
            self.update_service(params)
        else:
            self.create_service(params)

    def get_logs(self):
        if os.path.exists(self.log_file):
            with open(self.log_file, 'rb') as file:
                raw_data = file.read()
            detection = chardet.detect(raw_data)
            encoding = detection['encoding']
            confidence = detection['confidence']
            if confidence < 0.9:  # 示例阈值，根据需要调整
                encoding = 'GBK'  # 或选择另一个可能的编码
            try:
                return raw_data.decode(encoding, errors='ignore')
            except UnicodeDecodeError:
                return "Failed to decode the log file with detected encoding."
        return "Log file does not exist."
