from datetime import datetime
import os

"""
This class deals with logging.
Create instance of Logger class and you can use info, error or debug methods.
Log file will be created in the same directory as your module.
"""

class Logger:
    log_location = "default"
    log_module = "default"

    def __init__(self, log_location, log_module):
        """
        Need to supply:
        log_location - This is path where your module is located.
        log_module - This is the name of the module you are trying to log.
        """
        self.log_location = log_location
        self.log_module = log_module

    def get_timestamp(self):
        current_time = datetime.now()
        timestamp_str = current_time.strftime("%Y-%m-%d-%H-%M-%S")
        return timestamp_str

    def message_stem(self):
        message_string = self.get_timestamp() + "\t" + self.log_module + "\t"
        return message_string

    def write_log(self, message):
        logfile = os.path.join(self.log_location, "logging.txt")
        with open(logfile, "a") as logging:
            logging.write(message)

    def info(self, message):
        log_message = self.message_stem() + "INFO" + "\t" + message + "\n"
        self.write_log(log_message)

    def error(self, message):
        log_message = self.message_stem() + "ERROR" + "\t" + message + "\n"
        self.write_log(log_message)

    def debug(self, message):
        log_message = self.message_stem() + "DEBUG" + "\t" + message + "\n"
        self.write_log(log_message)        