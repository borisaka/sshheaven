""" Module with value objects - learinng to avoid boilerplates """
import enum
import abc

from vpnheaven.common import BasicStruct

class ActionState(enum.Enum):
    """ States for pty task"""
    PENDING = 0 
    RUNNING = 50 
    EXPECTING_RESULT = 70 
    DONE = 100
    FAILED = -10

#TODO make state numbers correspond to EXITCODES
class ActionResultState(enum.Enum):
    """ Represent UNIX errorcodes (actualy only 0 and 1) """
    SUCCESS = 0
    ERROR = 1
    CONNECTION_PROBLEMS = 10
    TEMPORARY_UNAVAILABLE = 20
    TIMEOUT = 40
    UNACCEPTABLE = -10 


class Action(BasicStruct):
    """ Action is a elementary SHELL command with some purpose
    command 
    """
    def __init__(self, command, callback=None, errback=None):
        BasicStruct.__init__(self, command)


class ActionProgress(BasicStruct):
    """ Keep state and loggin stdout about progress about started action """
    def __init__(self, state, raw_output):
        BasicStruct.__init__(self, state, raw_output)


class ActionResult(BasicStruct):
    """ Finished/Failed task. keeps app state, prcess exit code,
    and handled by user callback results"""
    def __init__(self, state, exit_code, handled_result, handled_errors):
        BasicStruct.__init__(self, state, exit_code, handled_result, handled_errors)


