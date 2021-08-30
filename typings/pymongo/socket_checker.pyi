"""
This type stub file was generated by pyright.
"""

import select
import sys

"""Select / poll helper"""
_HAVE_POLL = hasattr(select, "poll") and not sys.platform.startswith('java')
_SelectError = getattr(select, "error", OSError)
class SocketChecker(object):
    def __init__(self) -> None:
        ...
    
    def select(self, sock, read=..., write=..., timeout=...):
        """Select for reads or writes with a timeout in seconds (or None).

        Returns True if the socket is readable/writable, False on timeout.
        """
        ...
    
    def socket_closed(self, sock):
        """Return True if we know socket has been closed, False otherwise.
        """
        ...
    

