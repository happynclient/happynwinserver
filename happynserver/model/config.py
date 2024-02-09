"""
# 示例用法
config_manager = HPYConfigManager()

# 设置默认配置
default_config = {
    "服务器端口": 8080,
    "服务ID": "DefaultServiceID",
    "服务子网": "255.255.255.0",
    "自定义参数": "DefaultValue",
    "是否开机自启动": 1,
    "是否最小化到托盘": 1
}

# 使用默认配置初始化或更新注册表
config_manager.update(default_config)

# 读取特定配置项，如果不存在则使用默认值
server_port = config_manager.get("服务器端口", 8080)

# 修改配置项
config_manager.set("服务器端口", 9090)

# 删除配置项
config_manager.delete("自定义参数")
"""

import winreg as reg

class HPYConfigManager:
    def __init__(self, base_key_path="SOFTWARE\\HappynServer\\Parameters"):
        self.base_key_path = base_key_path
        self.config = self.load_config()

    def load_config(self):
        """从注册表加载配置到字典"""
        config = {}
        try:
            with reg.OpenKey(reg.HKEY_CURRENT_USER, self.base_key_path, 0, reg.KEY_READ) as key:
                i = 0
                while True:
                    try:
                        value_name, value_data, _ = reg.EnumValue(key, i)
                        config[value_name] = value_data
                        i += 1
                    except WindowsError:
                        break
        except WindowsError:
            pass  # 如果指定路径不存在，则忽略错误
        return config

    def save_config(self):
        """将字典中的配置保存到注册表"""
        try:
            with reg.CreateKey(reg.HKEY_CURRENT_USER, self.base_key_path) as key:
                for name, data in self.config.items():
                    reg.SetValueEx(key, name, 0, reg.REG_SZ if isinstance(data, str) else reg.REG_DWORD, data)
        except WindowsError as e:
            print(f"Error saving config to registry: {e}")

    def get(self, name, default=None):
        """获取指定名称的配置项，如果不存在，则返回默认值"""
        return self.config.get(name, default)

    def set(self, name, value):
        """设置配置项"""
        self.config[name] = value
        self.save_config()

    def delete(self, name):
        """删除配置项"""
        if name in self.config:
            del self.config[name]
            self.save_config()

    def update(self, updates):
        """更新多个配置项"""
        self.config.update(updates)
        self.save_config()

