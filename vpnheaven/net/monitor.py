class Monitor:
    def init(self, ssh_context):
        self.ssh = ssh_context
        self.origin_interfaces= self.load_interfaces

    def load_interfaces(self):
        return list(self.ssh.exec_command("ifconfig | grep -Eo '^\w+'"))

    def new_interfaces(self):
        all = self.load_interfaces()
        returnfilter(lambda i: i not in self)

