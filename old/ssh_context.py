from paramiko import SSHClient, AutoAddPolicy
from scp import SCPClient
import config
class SSHContext:
    def __init__(self, server, username, password):
        self.client = SSHClient()
        self.client.set_missing_host_key_policy(AutoAddPolicy)
        self.client.connect(server, username=username, password=password)
        self.client.exec_command("sh -l")
        self.use_sudo = config.use_sudo 
        self.env_path = config.env_path 

    def exec_command(self, cmd):
        _, ssh_stdout, _ = self._exec(cmd)
        for line in ssh_stdout:
            config.logger.debug(line)
            yield line

    def _exec(self, cmd):
        if self.use_sudo:
            cmd = "sudo %s" % cmd
        return self.client.exec_command(cmd)


    def upload_file(self, file_path, new_file_path=None):
        remote_file_name = new_file_path or file_path.split("/")[-1]
        scp = SCPClient(self.client.get_transport())
        scp.put(file_path, remote_file_name)

if __name__ == "__main__":
    context = SSHContext(config.ssh_host, config.ssh_user, config.ssh_password)
    context.exec_command("ls -la")
