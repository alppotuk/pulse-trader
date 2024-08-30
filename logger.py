import logging

class Logger:
    def __init__(self, name):
        self.name = name + "Logger"
        self.logger = logging.getLogger(self.name)
        self.logger.setLevel(logging.DEBUG)

        console_handler = logging.StreamHandler()
        file_handler = logging.FileHandler(self.name + ".log")

        console_handler.setLevel(logging.DEBUG)
        file_handler.setLevel(logging.DEBUG)

        console_format = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
        file_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

        console_handler.setFormatter(console_format)
        file_handler.setFormatter(file_format)

        self.logger.addHandler(console_handler)
        self.logger.addHandler(file_handler)

        self.logger.info(self.name + " initialized.")

    def log(self, level, message):
        if level == "info":
            self.logger.info(message)
        elif level == "warning":
            self.logger.warning(message)
        elif level == "error":
            self.logger.error(message)
        elif level == "debug":
            self.logger.debug(message)
        else:
            self.logger.info(message) 