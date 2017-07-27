from datetime import datetime
import re
import paramiko
from actions import  Action, ActionProgress, ActionResult, ActionState, ActionResultState

class Actor:
    """Actor acts actions, produced by producer=)
    Actor created with action to perform and channel when perform 
    Full execution cycle actor yields intermediate and final results 
    to producer
    """
    def __init__(self, channel, action):
        """ chanel is a single session of SSH connection.
        action is a actions.Action instance """
        self.channel = channel
        self.action = action

    def act(self):
        """Executes shell command from action. yields to producer.
        Waiting for shell promt brefore and after running"""
        self.progress = ActionProgress(self.action, ActionState.AWAITING_PROMT, [])
        yield self._step_progress()
        self.await_promt()
        yield self._step_progress()
        self._send_command(self.action.command)
        self.await_promt()
        yield self._step_progress
        # TODO Make failure handling to 
        result = ActionResult(ActionResultState.SUCCESS, 0, progress.raw_output, [])
        yield (self.action, progress, result)

    def await_promt(self):
        promt = re.compile('%s:.*%s\$ ?' % (config.hostname, config.username))
        self.await_tty_value(promt, lambda out: progress.raw_output.append(out))

    def await_tty_value(self, regex, started=datetime.utcnow()):
        if (datetime.utcnow() - started).seconds > config.timeout:
            raise "TIME!!!"
        for line in self._collect_output():
            if regex.match(line):
                yield line

    def _step_progress(self):
        states = ActionProgress.__members__.values()
        next_state = states[states.index(self.progress.state) + 1]
        self.progress.state = next_state
        return (self.action, self.progress)

    def _send_command(self, cmd):
        self.channel.send(cmd + "\n")

    def _collect_output(self):
        while self.channel.recv_ready():
            chunk = self.channel.recv(1024).split("\n")
            for line in chunk:
                print line 
                yield line

class Producer:
    def __init__(self):
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.client.AutoAddPolicy)
        ssh.connect(config.ssh_host, username=config.username)
        # cls.promt_matcher = re.compile("%s\$$" % config.username)
        self.__connection = ssh
        self._actors = []

    def produce_action(self, action):
        actor = Actor(self._produce_channel(), action)
        for stage in actor.act():
            self._produce_reports(self.stage)
            
    def _produce_channel(self):
        channel = self.__connection().get_transport().open_session()
        channel.get_pty()
        channel.exec_command("sh -l\n")
        return channel

    def _produce_reports(self, stage):
        print "STDOUT REPORT: %s" % stage

