import os
import paramiko
from vpnheaven.action.actor import Actor
from vpnheaven.action.actions import *
SSH_HOST = "localhost"
SSH_USER = os.getlogin()

class TestActor:

    def test_collect_output(self):
        self.mk_client()
        lines = []
        self.channel.send(self.action.command)
        for out in self.actor._collect_output():
            lines.append(out)
            print out

    def mk_client(self):
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.client.AutoAddPolicy)
        ssh.connect(SSH_HOST, username=SSH_USER)
        self.channel = ssh.get_transport().open_session()
        self.channel.get_pty()
        self.channel.exec_command("sh -l\n")
        self.action = Action("./tests/libexec/success.py")
        self.actor = Actor(self.channel, self.action)
