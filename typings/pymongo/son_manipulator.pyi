"""
This type stub file was generated by pyright.
"""

"""**DEPRECATED**: Manipulators that can edit SON objects as they enter and exit
a database.

The :class:`~pymongo.son_manipulator.SONManipulator` API has limitations as a
technique for transforming your data. Instead, it is more flexible and
straightforward to transform outgoing documents in your own code before passing
them to PyMongo, and transform incoming documents after receiving them from
PyMongo. SON Manipulators will be removed from PyMongo in 4.0.

PyMongo does **not** apply SON manipulators to documents passed to
the modern methods :meth:`~pymongo.collection.Collection.bulk_write`,
:meth:`~pymongo.collection.Collection.insert_one`,
:meth:`~pymongo.collection.Collection.insert_many`,
:meth:`~pymongo.collection.Collection.update_one`, or
:meth:`~pymongo.collection.Collection.update_many`. SON manipulators are
**not** applied to documents returned by the modern methods
:meth:`~pymongo.collection.Collection.find_one_and_delete`,
:meth:`~pymongo.collection.Collection.find_one_and_replace`, and
:meth:`~pymongo.collection.Collection.find_one_and_update`.
"""
class SONManipulator(object):
    """A base son manipulator.

    This manipulator just saves and restores objects without changing them.
    """
    def will_copy(self):
        """Will this SON manipulator make a copy of the incoming document?

        Derived classes that do need to make a copy should override this
        method, returning True instead of False. All non-copying manipulators
        will be applied first (so that the user's document will be updated
        appropriately), followed by copying manipulators.
        """
        ...
    
    def transform_incoming(self, son, collection):
        """Manipulate an incoming SON object.

        :Parameters:
          - `son`: the SON object to be inserted into the database
          - `collection`: the collection the object is being inserted into
        """
        ...
    
    def transform_outgoing(self, son, collection):
        """Manipulate an outgoing SON object.

        :Parameters:
          - `son`: the SON object being retrieved from the database
          - `collection`: the collection this object was stored in
        """
        ...
    


class ObjectIdInjector(SONManipulator):
    """A son manipulator that adds the _id field if it is missing.

    .. versionchanged:: 2.7
       ObjectIdInjector is no longer used by PyMongo, but remains in this
       module for backwards compatibility.
    """
    def transform_incoming(self, son, collection):
        """Add an _id field if it is missing.
        """
        ...
    


class ObjectIdShuffler(SONManipulator):
    """A son manipulator that moves _id to the first position.
    """
    def will_copy(self):
        """We need to copy to be sure that we are dealing with SON, not a dict.
        """
        ...
    
    def transform_incoming(self, son, collection):
        """Move _id to the front if it's there.
        """
        ...
    


class NamespaceInjector(SONManipulator):
    """A son manipulator that adds the _ns field.
    """
    def transform_incoming(self, son, collection):
        """Add the _ns field to the incoming object
        """
        ...
    


class AutoReference(SONManipulator):
    """Transparently reference and de-reference already saved embedded objects.

    This manipulator should probably only be used when the NamespaceInjector is
    also being used, otherwise it doesn't make too much sense - documents can
    only be auto-referenced if they have an *_ns* field.

    NOTE: this will behave poorly if you have a circular reference.

    TODO: this only works for documents that are in the same database. To fix
    this we'll need to add a DatabaseInjector that adds *_db* and then make
    use of the optional *database* support for DBRefs.
    """
    def __init__(self, db) -> None:
        ...
    
    def will_copy(self):
        """We need to copy so the user's document doesn't get transformed refs.
        """
        ...
    
    def transform_incoming(self, son, collection):
        """Replace embedded documents with DBRefs.
        """
        ...
    
    def transform_outgoing(self, son, collection):
        """Replace DBRefs with embedded documents.
        """
        ...
    


