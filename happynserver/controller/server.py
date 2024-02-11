import socket

class ServerManager:
    def __init__(self, server_address="127.0.0.1"):
        self.server_address = server_address

    def send_stop_signal(self, port):
        # 创建 UDP 套接字
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
            try:
                # 设置服务器地址和端口
                server = (self.server_address, port)
                # 发送停止信号
                message = "stop".encode('utf-8')  # 将字符串编码为字节
                sent = sock.sendto(message, server)
                return 0 if sent == len(message) else 1
            except Exception as e:
                print(f"Failed to send stop signal: {e}")
                return 1