# Updated customLogger.py
import logging
import os
from datetime import datetime

class LogGen:
    logger = None
    log_file_path = None

    @staticmethod
    def loggen():
        if LogGen.logger is None:
            log_dir = os.path.join(os.getcwd(), "Logs")
            os.makedirs(log_dir, exist_ok=True)

            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            log_filename = f"automation_{timestamp}.log"
            LogGen.log_file_path = os.path.join(log_dir, log_filename)

            logger = logging.getLogger("SCHProjectLogger")
            logger.setLevel(logging.DEBUG)

            file_handler = logging.FileHandler(LogGen.log_file_path, mode='w')
            formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
            file_handler.setFormatter(formatter)

            if not logger.handlers:
                logger.addHandler(file_handler)

            LogGen.logger = logger

        return LogGen.logger

    @staticmethod
    def clear_old_logs():
        log_dir = os.path.join(os.getcwd(), "Logs")
        if os.path.exists(log_dir):
            for filename in os.listdir(log_dir):
                file_path = os.path.join(log_dir, filename)
                try:
                    os.remove(file_path)
                except Exception as e:
                    print(f"Could not delete log file {file_path}: {e}")

    @staticmethod
    def close_logger():
        if LogGen.logger:
            for handler in LogGen.logger.handlers:
                handler.close()
                LogGen.logger.removeHandler(handler)
            LogGen.logger = None
