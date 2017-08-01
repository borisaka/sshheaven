from abc import ABCMeta
import inspect 
class BasicStruct():
    """Lazy to make self.x = x on every data class"""
    __metaclass__ = ABCMeta

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
