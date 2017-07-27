from provider import Provider
from common import LoggerStateStream
from  ssh_context import SSHContext
import config
import tempfile
class VpnManager:
    def __init__(self, state_stream):
        self.state_stream = state_stream
        self.ssh_context = SSHContext(config.ssh_host, config.ssh_user, config.ssh_password)
        self.provider = Provider(self.ssh_context, config.allow_countries or [], config.reject_countries or [])

    def connect(self):
        self.state_stream.notify(0.1, "Ensure disconnected all")
        self.provider.disconnect_all()
        self.state_stream.notify(0.2, "Detecting best server")
        self.server = self.provider.find_server()
        h = self.server
        self.state_stream.notify(0.5, "Connecting to %s in %s(%s)" %(h.ip, h.country_long, h.country_short))
        self.provider.history_put(self.server.ip)
        self.provider.connect(self.server)
        self.state_stream.notify(1, "Connected")

if __name__ == "__main__":
    manager = VpnManager(LoggerStateStream(config.logger))
    manager.connect()

