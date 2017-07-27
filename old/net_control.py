class NetControl:
    def __init__(self, ssh_context):
        self.ssh = ssh_context
        self.initial_interfaces = self._detect_interfaces() 

    def extra_interfaces(self):
        filter(lambda i: i not in self.initial_interfaces, self._detect_interfaces())

    def _detect_interfaces(self):
        return [ i.split(":")[0] for i in self.ssh.exec_command("ifconfig | grep -o '^\w*:'")]

