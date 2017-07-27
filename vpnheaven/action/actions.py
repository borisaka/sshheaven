""" Module with value objects - learinng to avoid boilerplates """
import inspect 
import enum
import abc

class BasicStruct():
    """Lazy to make self.x = x on every data class"""
    __metaclass__ = abc.ABCMeta

    @classmethod
    def fields(cls):
        constructor = cls.__dict__['__init__']
        return inspect.getargspec(constructor).args[1:]

    # TODO Smells like monkey code 
    # Don't you believe, what Interpreter verify arguments on method call?
    # I hope so, but I scared. I breaks using metaprogramming on python in school years
    def __init__(self, *args, **kwargs):
        fields = self.fields()
        for i,arg in enumerate(args):
            setattr(self, fields[i], arg)
        for k,v in kwargs.iteritems():
            if getattr(self, k):
                raise "Property %s already defined.... Error prevents from debug hell"
            if not k in fields:
                raise "Propery %s is not defined in __init__ is it correct? then override this"
            setattr(self, k, v)

    def __str__(self):
        class_name = self.__class__.__name__
        str_attrs = ",".join(["%s=%s" %(k,v) for k,v in self.__dict__.iteritems()])
        return "%s(%s)" %(class_name, str_attrs)

    def __repr__(self):
        return self.__str__()


class ActionState(enum.Enum):
    """ States for pty task"""
    PENDING = 0 
    AWAITING_PROMT = 10
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
        BasicStruct.__init__(self, action, progress, state, exit_code, handled_result, handled_errors)


