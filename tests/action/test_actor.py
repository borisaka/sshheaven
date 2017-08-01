import os
import paramiko
from vpnheaven.action.actor import Actor
from vpnheaven.action.actions import *
import time
SSH_HOST = "localhost"
SSH_USER = "fin" 

class TestActor:
    def test_collect_output(self):
        self.mk_client()
        lines = []
        self.channel.send(self.action.command)
        ic = self.channel.recv(1024)
        assert len(ic) < 100
        for out in self.actor._collect_output():
            lines.append(out)

    def mk_client(self):
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.client.AutoAddPolicy)
        ssh.connect(SSH_HOST, username=SSH_USER)
        self.channel = ssh.get_transport().open_session()
        self.channel.get_pty()
        self.action = Action("")
        self.actor = Actor(self.channel, self.action)
