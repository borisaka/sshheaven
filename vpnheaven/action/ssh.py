from time import time
import paramiko
import pubsub
from vpnheaven.common import BasicStruct
from vpnheaven.action.actions import ActionState

class Session:
    def __init__(self,rules):
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.client.AutoAddPolicy)
        ssh.connect(rules.host, username=rules.username)
        # cls.promt_matcher = re.compile("%s\$$" % self.rules.username)
        self.ssh = ssh
        self.processes = []

    def start_process(self, cmd):
        with_watch = '%s & echo "pid: ||$!||"'
        si, so, se = self.ssh.exec_command(cmd)
        proc = Process(si,so,se)
        processes.append(Process(si,so,se))



class Process(BasicStruct):
    def __init__(self, sin, sout, serr):
        BasicStruct.__init__(self, pid, sin, sout, serr)
        self.state = ActionState.PENDING
        self.started= time()
        self.sout_log = []
        self.serr_log = []

    def update
        self.check_io_status()

    # def check(self):
    #     self._recv_io_data(self.sout, self.sout_log)
    #     self._recv_io_data(self.serr, self.serr_log)
    #     self._check_io_status(self.sout.channel)

    def check_io_status(self, channel):
        if channel.closed:
            self.exit_status = channel.exit_status_ready() and channel.exit_status 
            if self.exit_status > 0:
                self.state = ActionState.FAILED
            else:
                self.state = ActionState.DONE
            self.ended = time.time() 
            return false
        else:
            self.state = ActionState.RUNNING 
            return true

     def recv_io_data(self, channel, log):
        while channel.recv_ready():
            for line in channel.recv(1024).split("/n")
                yield line 
        

    # def handle_result(self, std_threads):
        
        
