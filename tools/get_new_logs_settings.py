import logging
import os.path
from logging.handlers import TimedRotatingFileHandler
from config.paths import LOGS_PATH

ROTATION_TIME = 1
HOURS_PER_DAY = 24
DAYS_TO_KEEP = 7


def start_logger(log_level: int = logging.INFO) -> logging.Logger:
    """
    Creates a root logger that logs to a file and to the console. File is rotated every hour and backed up for
    168 hours (7 days).
    :param log_level:
    :return:
    """
    function_logs_path = os.path.join(LOGS_PATH, 'logs')

    if not os.path.exists(LOGS_PATH):
        os.makedirs(LOGS_PATH)

    if not os.path.exists(function_logs_path):
        os.makedirs(function_logs_path)

    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)

    log_file_path = os.path.join(function_logs_path, 'logfile.log')

    time_rotate_handler = TimedRotatingFileHandler(filename=log_file_path,
                                                   when="h",
                                                   interval=ROTATION_TIME,
                                                   backupCount=HOURS_PER_DAY * DAYS_TO_KEEP)
    stream_handler = logging.StreamHandler()
    console_formatter = logging.Formatter('%(asctime)s - %(levelname)s: %(message)s')
    stream_handler.setFormatter(console_formatter)
    file_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    time_rotate_handler.setFormatter(file_formatter)
    root_logger.addHandler(time_rotate_handler)
    root_logger.addHandler(stream_handler)
    return root_logger
