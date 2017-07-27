#! /usr/bin/env python2.7
from paramiko.client import SSHClient, AutoAddPolicy
from scp import SCPClient
import sys
import subprocess
import config
def connection():
    client = SSHClient()
    client.set_missing_host_key_policy(AutoAddPolicy)
    client.connect(config.ssh_host, username=config.ssh_user, password=config.ssh_password)
    return client

def exec_cmd(cmd):
    conn = connection()
    if config.use_sudo:
        cmd = "sudo %s" % cmd 
    ssh_stdin, ssh_stdout, ssh_stderr = conn.exec_command("/bin/sh -c 'PATH=%s %s'" % (config.env_path, cmd))
    print ssh_stdout.read()
    print ssh_stderr.read()

