from ifcb import DataDirectory

from storage.utils import ObjectStore
from storage.config_builder import register_store

@register_store
class IFCBHeadersStore(ObjectStore):
    """ Readonly store for accessing IFCB data. """

    def __init__(self, data_dir: str):
        super().__init__()
        self.data_dir = data_dir

    def get(self, key) -> bool:
        """ Get the bin data for a specified bin """
        data_dir = DataDirectory(self.data_dir)
        ifcb_bin = data_dir[key]
        return ifcb_bin.headers

    def exists(self, key) -> bool:
        data_dir = DataDirectory(self.data_dir)
        return data_dir.has_key(key)

    def put(self, key, value):
        """Put is not supported for readonly store."""
        raise NotImplementedError("Put operation is not supported for IfcbRoiStore.")

    def delete(self, key):
        """Delete is not supported for readonly store."""
        raise NotImplementedError("Delete operation is not supported for IfcbRoiStore.")
