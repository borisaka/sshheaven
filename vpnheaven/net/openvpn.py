import re, time
from net import Protocol
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
        
    # def __load_settings(self):
    #     nocoment = re.compile('^[^ (#|;)].*', re.MULTILINE)
    #     lines = [line.strip() for line in nocoment.findall(self.file_content) if len(line.strip()) > 0]
    #     settings = [re.search('(^\w+) (.*)', l).groups() for l in filter(lambda line: re.match('^\w* ', line), lines)]
    #     self.devise = ['dev']
        # self.protocol = getattr(Protocol, hsh['protocol'].upper())
        # self.host, self.port = hsh['remote'].split(' ')
class Session:
    def __init__(self, config, ssh_context):
        self.config = config
        self.state = 'offline'
        self.ssh = ssh_context

    def start(self):
        self.config_name = "config_%s.ovpn" % time.time() 
        self.config_path = "./tmp/%s" % self.config_name
        self._export_config()
        self._connect()

    def _export_config(self):
        with open(self.config_path, "w") as f:
            f.write(self.config.file_content)
        self.ssh.upload_file(self.config_path, "/tmp/%s" % self.config_name)

    def _connect(self):
        self.ssh.exec_command("openvpn --config /tmp/%s" % self.config_name)


