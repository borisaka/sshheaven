import os, base64, threading

class VpnHost():
    def __init__(self, ip, country_short, country_long, log_type, config):
        self.ip = ip
        self.country_short = country_short
        self.country_long = country_long
        self.log_type = log_type
        self.config = base64.b64decode(config)
    
    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return "%s %s log_type: %s" % (self.ip, self.country, self.log_type)

class LoggerStateStream:
    def __init__(self, logger):
        self.logger = logger

    def notify(self, state, msg):
        self.logger.debug("%d %s" % (state, msg))

class ThreadedConnector(threading.Thread):
    def __init__(self, manager):
        threading.Thread.__init__(self)
        self.manager = manager

    def run(self):
        self.manager.connect()
