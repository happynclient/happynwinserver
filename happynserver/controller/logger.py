import logging
import os


# 定义日志的配置函数
def setup_logger(log_file=None):
    if not log_file:
        programdata_path = os.getenv('PROGRAMDATA')
        log_file = os.path.join(programdata_path, "happynet", 'HappynServerDebug.log')
        print('ProgramData Log Path:', log_file)
        # 检查日志文件的目录是否存在，如果不存在，则创建
        log_dir = os.path.dirname(log_file)
        if not os.path.exists(log_dir):
            os.makedirs(log_dir, exist_ok=True)  # 使用exist_ok=True避免在目录已存在时引发异常

        # 检查日志文件是否存在，如果不存在，则创建
        if not os.path.exists(log_file):
            with open(log_file, 'a') as log_file_set:  # 使用'a'模式打开文件，如果文件不存在将会被创建
                pass  # 不需要在文件中写入任何内容，仅确保文件存在

    # 获取一个logger对象
    logger = logging.getLogger('simple_logger')
    logger.setLevel(logging.DEBUG)  # 设置日志级别

    # 创建一个文件处理器，并设置级别和格式化器
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)

    # 添加文件处理器到logger
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