"""
This type stub file was generated by pyright.
"""

"""Tools for working with read concerns."""
class ReadConcern(object):
    """ReadConcern

    :Parameters:
        - `level`: (string) The read concern level specifies the level of
          isolation for read operations.  For example, a read operation using a
          read concern level of ``majority`` will only return data that has been
          written to a majority of nodes. If the level is left unspecified, the
          server default will be used.

    .. versionadded:: 3.2

    """
    def __init__(self, level=...) -> None:
        ...
    
    @property
    def level(self):
        """The read concern level."""
        ...
    
    @property
    def ok_for_legacy(self):
        """Return ``True`` if this read concern is compatible with
        old wire protocol versions."""
        ...
    
    @property
    def document(self):
        """The document representation of this read concern.

        .. note::
          :class:`ReadConcern` is immutable. Mutating the value of
          :attr:`document` does not mutate this :class:`ReadConcern`.
        """
        ...
    
    def __eq__(self, other) -> bool:
        ...
    
    def __repr__(self):
        ...
    


DEFAULT_READ_CONCERN = ReadConcern()