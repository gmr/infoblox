"""Infoblox Exceptions"""

class ProtocolError(Exception):

    def __repr__(self):
        return '<%s %s>' % (self.__class__.__name__, self.args[1])
