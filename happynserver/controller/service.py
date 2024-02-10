"""
# 示例用法
# 无论调用多少次ServiceManager，返回的都是同一个实例
service_manager1 = ServiceManager("MyService", "python my_service.py --port {port} --id {service_id}")
service_manager2 = ServiceManager("MyService", "python my_service.py --port {port} --id {service_id}")
assert service_manager1 is service_manager2  # 这将证明service_manager1和service_manager2是同一个实例
"""
import subprocess
import os


class SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(SingletonMeta, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class ServiceManager(metaclass=SingletonMeta):
    def __init__(self, service_name, command_template):
        self.service_name = service_name
        self.command_template = command_template
        self.log_file = f"{service_name}.log"
        self.service_status = 0

    def create_service(self, params):
        command = self.command_template.format(**params) + f" > {self.log_file} 2>&1"
        create_command = f'sc create {self.service_name} binPath= "{command}" start= auto'
        # subprocess.run(create_command, shell=True)

    def start_service(self):
        # subprocess.run(f'sc start {self.service_name}', shell=True)
        self.service_status = 1

    def stop_service(self):
        # subprocess.run(f'sc stop {self.service_name}', shell=True)
        self.service_status = 0

    def delete_service(self):
        self.stop_service()
        # subprocess.run(f'sc delete {self.service_name}', shell=True)
        self.service_status = 0

    """Return: 1 running
               0 stopped
    """
    def get_service_status(self):
        return self.service_status

    def update_service(self, params):
        self.delete_service()
        self.create_service(params)

    def get_logs(self):
        if os.path.exists(self.log_file):
            with open(self.log_file, 'r') as file:
                return file.read()
        return "Log file does not exist."
