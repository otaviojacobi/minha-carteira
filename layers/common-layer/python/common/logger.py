import logging
import os


class Logger:

    def __init__(self, name=None):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(os.environ['LOG_LEVEL'])

    def instance(self):
        return self.logger
