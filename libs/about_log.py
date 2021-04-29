# 生动态成日志
import logging.handlers
import logging


class GetLog:
    def __init__(self, log_path, log_filename):
        self.log_filename = log_filename
        self.log_path = log_path
        self.logger = None

    def log(self):
        if self.logger is None:
            self.logger = logging.getLogger()
            self.logger.setLevel(logging.INFO)

            fm = "%(asctime)s:%(levelname)s:%(name)s:%(filename)s:%(lineno)d:%(message)s"
            fmt = logging.Formatter(fm)
            cl = logging.handlers.TimedRotatingFileHandler("{}/{}.log".format(self.log_path, self.log_filename),
                                                           when="W0",
                                                           interval=10,
                                                           encoding="utf8")
            cl.setLevel(logging.INFO)
            cl.setFormatter(fmt)

            self.logger.addHandler(cl)
        return self.logger
