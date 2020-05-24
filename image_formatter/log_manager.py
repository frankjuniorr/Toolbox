from datetime import datetime
import os
import logging
from enum import Enum

class LogManager:

    _instance = None
    _logger_duplicate = None

    # ============================================
    @classmethod
    def instance(self):
        if self._instance is None:
            self._instance = self()
        return self._instance

    # ============================================
    def __init__(self):
        _home = os.environ['HOME']
        self.log_path = f"{_home}/log/image_formatter"

    # ============================================
    @property
    def getLoggerDuplicateFile(self):
        if self._logger_duplicate is None:
            self._logger_duplicate = self.configure_log("log_file_duplicate", self.get_log_path())
        return self._logger_duplicate

    # ============================================
    def configure_log(self, name, log_file):
        """
        Function that configure Log
        """
        formatter = logging.Formatter('%(message)s')
        handler = logging.FileHandler(log_file)
        handler.setFormatter(formatter)

        logger = logging.getLogger(name)
        logger.setLevel(logging.DEBUG)
        logger.addHandler(handler)

        return logger

    # ============================================
    def get_log_path(self):
        """
        Function that return Log file path
        """
        log_date_format = '%Y-%m-%d_%H-%M-%S'
        log_date_time = datetime.now().strftime(log_date_format)

        if not os.path.exists(self.log_path):
            os.makedirs(self.log_path)

        log_file = f"{self.log_path}/{log_date_time}_duplicated_files.log"

        return log_file

    # ============================================
    def log_clean(self):
        """
        Function that remove log file if file is empty
        """
        EMPTY = 0

        log_file = self.get_log_path()

        if os.path.isfile(log_file) and \
            os.path.getsize(log_file) == 0:
                os.remove(log_file)

        # if all log was cleaned, delete log folder
        log_folder = os.listdir(self.log_path)
        if len(log_folder) == EMPTY:
            os.rmdir(self.log_path)

