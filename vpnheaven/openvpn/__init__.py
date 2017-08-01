import re, time
from vpnheaven.net import Protocol
from vpnheaven import shell_utils 
class Server:
    def __init__(self, protocol, host, port):
        self.host = host
        self.protocol= protocol
        self.port = port
    def __str__(self):
        return "Server(%s %s:%d)" % (self.protocol, self.host, self.port)

    def __repr__(self):
        return self.__str__()

class Config:
    def __init__(self, path=None, content=None):
        if path and content:
            self.logger.warn("Config present path and content both. USING path IGNORING content")
        if path:
            self.file_path = path
            content = open(path, 'r').read()
        self.file_content = content 
        self.devise = self.get_setting("dev")[0]
        proto = getattr(Protocol, self.get_setting("proto")[-1].upper())
        def mk_server(remote): 
            r = remote.split(" ")
            return Server(proto, r[0], int(r[1]))
        self.servers = [mk_server(remote) for remote in self.get_setting("remote")]
        

    def get_setting(self, setting):
        reg = re.compile("(^%s) (.*)$" % setting, re.MULTILINE)
        matches = [tpl[1].strip() for tpl in reg.findall(self.file_content)]
        return matches

    def __str__(self):
        return "openvpn.Config(devise=%s servers=%s)" % (self.devise, ";".join(map(str, self.servers)))
    def __repr__(self):
        return str(self)
        
class Session:
    def __init__(self, config):
        self.config = config
        # self.state = 'offline'

    def start(self):
        self.config_name = "config_%s.ovpn" % time.time() 
        self.config_path = "./tmp/%s" % self.config_name
        open(self.config_path, 'w').write(self.config.file_content)
        # self._export_config()
        # self._connect()
        shell_utils.upload_files(self.config_path, "/tmp/%s" % self.config_name)
        self.process = shell_utils.spawn(['/usr/local/sbin/openvpn', '--config', '/tmp/%s' % self.config_name])

    def kill(self):
        shell_utils.kill(self.process.pid)



