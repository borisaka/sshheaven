import paramiko
import threading
import config
class Connection:
    def __init__(self):

    def channel(self):
        ch = self.transport.open_session()
        return Session(ch) 



class Session:
    def __init__(self, channel):
        self.timeout = 30
        self.queue = []
        self.logger = config.logger
        self.channel = channel 
        self.channel.get_pty() 
        self.channel.exec_command("sh -l")
        self.process_stdout()

        
    def invoke(self, cmd):
        self.process_stdout()
        self.send_command(cmd)
        self.process_stdout()

    def send_command(self, cmd):
        self.channel.send(cmd)
        self.channel.send("\n")

    def process_stdout(self):
        for chunk in self.recv_stdout():
            self.logger.info(chunk)

    def recv_stdout(self):
        while self.channel.recv_ready():
            yield self.channel.recv(1024)

class Task:
    def __init__():
        pass

    def perform():
        self.state = "starting"
        
