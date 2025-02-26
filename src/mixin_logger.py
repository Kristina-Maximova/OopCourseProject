import logging

class MixinLogger:

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)
        self.filehandler = logging.FileHandler("..\\logs\\my_log_mixin.log","w", encoding="utf-8")
        self.file_formatter = logging.Formatter('%(asctime)s %(levelname)s %(filename)s %(funcName)s:%(message)s')
        self.filehandler.setFormatter(self.file_formatter)
        self.logger.addHandler(self.filehandler)

    def log_info(self, message):
        self.logger.info(message)

    def log_debug(self, message):
        self.logger.debug(message)

    def log_warning(self, message):
        self.logger.warning(message)

    def log_error(self, message):
        self.logger.error(message)