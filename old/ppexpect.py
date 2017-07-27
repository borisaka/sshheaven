from collections import namedtuple
import config
import paramiko
from paramiko_expect import SSHClientInteraction

class HostConfig:
    def __init__(self, hostname, username, home_dir):
        self.hostname = hostname
        self.username = username
        self.home_dir = home_dir
        self.initial_command = "sh -l"

    def promt(self, pwd="~"):
        promt = self.hostname + ":"
        if pwd in [self.home_dir]:
            promt += "~"
        else:
            promt += pwd.split("/")[-1]
        promt += " %s\$ ?" % self.username
        return promt 

def work():
    cfg = HostConfig('bm', 'b', '/Users/b')
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.client.AutoAddPolicy)
    client.connect(config.ssh_host, username=config.ssh_user)
    interact = SSHClientInteraction(client, timeout=10, display=True)
    interact.send(cfg.initial_command)
    # interact.expect(cfg.promt())
    return interact
