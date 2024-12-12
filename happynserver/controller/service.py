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

from .logger import setup_logger
logger = setup_logger()

HAPPYNSERVER_DESC = "HappynServer is a light VPN software which makes it "\
                    "easy to create virtual networks by passing intermediate firewalls. "\
                    "Powered by happyn.cn"

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

        programdata_path = os.getenv('PROGRAMDATA')
        self.log_file = os.path.join(programdata_path, "happynet", self.service_name+'.log')
        logger.info("ProgramData Log Path:{}".format(self.log_file))
        # 检查日志文件的目录是否存在，如果不存在，则创建
        log_dir = os.path.dirname(self.log_file)
        if not os.path.exists(log_dir):
            os.makedirs(log_dir, exist_ok=True)  # 使用exist_ok=True避免在目录已存在时引发异常

        # 检查日志文件是否存在，如果不存在，则创建
        if not os.path.exists(self.log_file):
            with open(self.log_file, 'a') as log_file:  # 使用'a'模式打开文件，如果文件不存在将会被创建
                pass  # 不需要在文件中写入任何内容，仅确保文件存在

        self.service_status = 0

    # nssm install <servicename> <program> [<arguments>]
    # nssm set <servicename> Description "xxxx"
    # nssm set <servicename> AppStdout <logpath>
    def create_service(self, params):
        create_command = f""" "{os.path.join(self.working_dir, 'utility', 'happynssm.exe')}" install {self.service_name} """ + \
                         f""" "{os.path.join(self.working_dir, 'utility', 'happynsupernode.exe')}" "{params}" """
        logger.info(create_command)
        subprocess.run(create_command, shell=True)

        setdesc_command = f""" "{os.path.join(self.working_dir, 'utility', 'happynssm.exe')}"  set {self.service_name} """ + \
                          f'Description "{HAPPYNSERVER_DESC}"'
        logger.info(setdesc_command)
        subprocess.run(setdesc_command, shell=True)

        setlog_command = f""" "{os.path.join(self.working_dir, 'utility', 'happynssm.exe')}"  set {self.service_name} """ + \
                         f'AppStdout {self.log_file}'
        logger.info(setlog_command)
        subprocess.run(setlog_command, shell=True)

        setlog_command = f""" "{os.path.join(self.working_dir, 'utility', 'happynssm.exe')}"  set {self.service_name} """ + \
                         f'AppStdoutCreationDisposition 4'
        logger.info(setlog_command)
        subprocess.run(setlog_command, shell=True)

        setlog_command = f""" "{os.path.join(self.working_dir, 'utility', 'happynssm.exe')}"  set {self.service_name} """ + \
                         f'AppStderrCreationDisposition 4'
        logger.info(setlog_command)
        subprocess.run(setlog_command, shell=True)

        setlog_command = f""" "{os.path.join(self.working_dir, 'utility', 'happynssm.exe')}"  set {self.service_name} """ + \
                         f'AppRotateFiles 1'
        logger.info(setlog_command)
        subprocess.run(setlog_command, shell=True)

        setlog_command = f""" "{os.path.join(self.working_dir, 'utility', 'happynssm.exe')}"  set {self.service_name} """ + \
                         f'AppRotateOnline 1'
        logger.info(setlog_command)
        subprocess.run(setlog_command, shell=True)

        setlog_command = f""" "{os.path.join(self.working_dir, 'utility', 'happynssm.exe')}"  set {self.service_name} """ + \
                         f'AppRotateSeconds 864000'
        logger.info(setlog_command)
        subprocess.run(setlog_command, shell=True)

        setlog_command = f""" "{os.path.join(self.working_dir, 'utility', 'happynssm.exe')}"  set {self.service_name} """ + \
                         f'AppRotateBytes 16777216'
        logger.info(setlog_command)
        subprocess.run(setlog_command, shell=True)


   # nssm.exe set <servicename> AppParameters <arguments>
    def update_service(self, params):
        update_command = f""" "{os.path.join(self.working_dir, 'utility', 'happynssm.exe')}" set {self.service_name} """ + \
                         f"""AppParameters "{os.path.join(self.working_dir, 'utility', 'happynsupernode.exe')}" "{params}" """
        logger.info(update_command)
        subprocess.run(update_command, shell=True)

    # nssm start <servicename>
    def start_service(self):
        start_command = f'"{os.path.join(self.working_dir, "utility", "happynssm.exe")}" start {self.service_name}'
        logger.info(start_command)
        subprocess.run(start_command, shell=True)

    def stop_service(self):
        stop_command = f'"{os.path.join(self.working_dir, "utility", "happynssm.exe")}" stop {self.service_name}'
        logger.info(stop_command)
        subprocess.run(stop_command, shell=True)

    #  nssm remove <servicename>
    def delete_service(self):
        if not self.is_service_exist():
            return
        if self.get_service_status() == 1:
            self.stop_service()
        delete_command = f'"{os.path.join(self.working_dir, "utility", "happynssm.exe")}" remove {self.service_name} confirm'
        logger.info(delete_command)
        subprocess.run(delete_command, shell=True)

    # nssm set <servicename> Start SERVICE_AUTO_START
    def set_service_auto_start(self):
        auto_start_command = f'"{os.path.join(self.working_dir, "utility", "happynssm.exe")}" ' + \
                             f'set {self.service_name} Start SERVICE_AUTO_START'
        logger.info(auto_start_command)
        subprocess.run(auto_start_command, shell=True)

    def unset_service_auto_start(self):
        unset_auto_start_command = f'"{os.path.join(self.working_dir, "utility", "happynssm.exe")}" ' + \
                             f'set {self.service_name} Start SERVICE_DEMAND_START'
        logger.info(unset_auto_start_command)
        subprocess.run(unset_auto_start_command, shell=True)

    """Return: 1 running
               0 stopped
    """
    def get_service_status(self):
        svc = None
        sch = None
        try:
            # 打开服务控制管理器
            sch = win32service.OpenSCManager(None, None, win32service.SC_MANAGER_ALL_ACCESS)

            # 打开指定的服务
            svc = win32service.OpenService(sch, self.service_name, win32service.SERVICE_QUERY_STATUS)

            # 查询服务状态
            status = win32service.QueryServiceStatusEx(svc)

            # 检查服务状态
            if status['CurrentState'] == win32service.SERVICE_RUNNING:
                self.service_status = 1
            else:
                self.service_status = 0
        except Exception as e:
            logger.error(f"Error: {e}")
            self.service_status = -1
        finally:
            # 关闭服务和服务控制管理器的句柄，确保句柄有效
            if svc:
                try:
                    win32service.CloseServiceHandle(svc)
                except Exception as e:
                    logger.error(f"Failed to close service handle: {e}")

            if sch:
                try:
                    win32service.CloseServiceHandle(sch)
                except Exception as e:
                    logger.error(f"Failed to close service control manager handle: {e}")

        return self.service_status

    def is_service_exist(self):
        is_exist = False
        svc = None
        sch = None
        try:
            # 打开服务控制管理器
            sch = win32service.OpenSCManager(None, None, win32service.SC_MANAGER_ALL_ACCESS)

            # 尝试打开指定的服务
            svc = win32service.OpenService(sch, self.service_name, win32service.SERVICE_QUERY_STATUS)

            # 查询服务状态
            status = win32service.QueryServiceStatusEx(svc)

            # 如果没有异常，服务存在
            is_exist = True
        except Exception as e:
            logger.error(f"Error: {e}")
            is_exist = False
        finally:
            # 关闭服务和服务控制管理器的句柄，确保句柄有效
            if svc:
                try:
                    win32service.CloseServiceHandle(svc)
                except Exception as e:
                    logger.error(f"Failed to close service handle: {e}")

            if sch:
                try:
                    win32service.CloseServiceHandle(sch)
                except Exception as e:
                    logger.error(f"Failed to close service control manager handle: {e}")

        return is_exist

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
