import logging
import os


# 定义日志的配置函数
# 定义检查和创建日志文件路径的函数
def ensure_log_path_exists(log_file):
    log_dir = os.path.dirname(log_file)
    if not os.path.exists(log_dir):
        try:
            os.makedirs(log_dir, exist_ok=True)
        except Exception as e:
            print(f"Error creating log directory {log_dir}: {e}")
            return False

    if not os.path.exists(log_file):
        try:
            with open(log_file, 'a'):
                pass
        except Exception as e:
            print(f"Error creating log file {log_file}: {e}")
            return False
    return True


# 定义日志的配置函数
def setup_logger(log_file=None):
    if not log_file:
        programdata_path = os.getenv('PROGRAMDATA')
        if not programdata_path:
            programdata_path = os.path.expanduser("~")  # 使用主目录作为备选路径

        log_file = os.path.join(programdata_path, "happynet", 'HappynServerDebug.log')
        print('ProgramData Log Path:', log_file)

        # 调用函数检查日志文件的目录和文件是否存在
        if not ensure_log_path_exists(log_file):
            return None  # 如果创建文件或目录失败，则返回

    logger_name = __name__
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.DEBUG)

    if not logger.handlers:
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger


# 使用log模块
if __name__ == '__main__':
    # 设置日志输出到log.txt文件
    log_file = 'log.txt'
    logger = setup_logger(log_file)

    # 写入几条日志数据
    logger.debug('这是一个 debug 级别的信息')
    logger.info('这是一个 info 级别的信息')
    logger.warning('这是一个 warning 级别的信息')
    logger.error('这是一个 error 级别的信息')
    logger.critical('这是一个 critical 级别的信息')

    print(f'日志已经记录到文件：{log_file}')