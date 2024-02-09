"""
# 示例用法
service_manager = ServiceManager("MyService", "python my_service.py --port {port} --id {service_id}")
service_manager.create_service({"port": 8080, "service_id": "service123"})
# service_manager.start_service()
# logs = service_manager.get_logs()
# print(logs)
# service_manager.stop_service()
# service_manager.delete_service()
"""
import subprocess
import os


class ServiceManager(object):
    def __init__(self, service_name, command_template):
        self.service_name = service_name
        self.command_template = command_template
        self.log_file = f"{service_name}.log"

    def create_service(self, params):
        command = self.command_template.format(**params) + f" > {self.log_file} 2>&1"
        create_command = f'sc create {self.service_name} binPath= "{command}" start= auto'
        subprocess.run(create_command, shell=True)

    def start_service(self):
        subprocess.run(f'sc start {self.service_name}', shell=True)

    def stop_service(self):
        subprocess.run(f'sc stop {self.service_name}', shell=True)

    def delete_service(self):
        subprocess.run(f'sc delete {self.service_name}', shell=True)

    def update_service(self, params):
        self.delete_service()
        self.create_service(params)

    def get_logs(self):
        if os.path.exists(self.log_file):
            with open(self.log_file, 'r') as file:
                return file.read()
        return "Log file does not exist."
