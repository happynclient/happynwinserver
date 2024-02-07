import yaml
from pathlib import Path
import platform

class HPYNConfigManager(object):
    def __init__(self):
        self.config_path = self.get_platform_config_path()
        self.configs = []

    def get_platform_config_path(self):
        # 确定平台特定的配置文件路径
        home = Path.home()
        if platform.system() == "Windows":
            return home / "AppData" / "Local" / "Happynet" / "config.yaml"
        elif platform.system() == "Darwin":
            return home / "Library" / "Application Support" / "Happynet" / "config.yaml"
        else:  # Linux and other Unix-like OS
            return home / ".happynet" / "config.yaml"

    def load_hpyn_config(self):
        if self.config_path.exists():
            with open(self.config_path, 'r') as file:
                self.configs = yaml.safe_load(file) or []

    def get_hpyn_configs(self):
        return self.configs

    def get_hpyn_config(self, index):
        return self.configs[index] if index < len(self.configs) else None

    def add_hpyn_config(self, config):
        self.configs.append(config)

    def remove_hpyn_config(self, index):
        if index < len(self.configs):
            self.configs.pop(index)

    def get_hpyn_config_parameter(self, index, param_name):
        config = self.get_hpyn_config(index)
        if config is not None:
            return config.get(param_name)
        return None

    def get_all_hpyn_config_parameters(self, index):
        config = self.get_hpyn_config(index)
        return config if config is not None else {}

    def save_hpyn_config(self):
        with open(self.config_path, 'w') as file:
            yaml.dump(self.configs, file)
