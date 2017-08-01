from vpnheaven.common import BasicStruct

class Rules(BasicStruct):
    def __init__(self, host, username, 
                 password=None, timeout=60):
        BasicStruct.__init__(self, host, username, password, timeout)
