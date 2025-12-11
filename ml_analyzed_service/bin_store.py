from ifcb import DataDirectory

from storage.utils import ObjectStore
from storage.config_builder import register_store


class BaseIFCBStore(ObjectStore):
    """Base class for readonly IFCB stores."""

    def __init__(self, data_dir: str):
        super().__init__()
        self.data_dir = data_dir

    def get(self, key):
        """Get data for a specified bin. Must be implemented by subclasses."""
        raise NotImplementedError("Subclasses must implement get method.")

    def exists(self, key) -> bool:
        data_dir = DataDirectory(self.data_dir)
        return data_dir.has_key(key)

    def put(self, key, value):
        """Put is not supported for readonly store."""
        raise NotImplementedError("Put operation is not supported for IfcbRoiStore.")

    def delete(self, key):
        """Delete is not supported for readonly store."""
        raise NotImplementedError("Delete operation is not supported for IfcbRoiStore.")


@register_store
class IFCBHeadersStore(BaseIFCBStore):
    """Readonly store for accessing IFCB header data."""

    def get(self, key):
        """Get the bin headers for a specified bin."""
        data_dir = DataDirectory(self.data_dir)
        ifcb_bin = data_dir[key]
        return ifcb_bin.headers


@register_store
class IFCBADCFileStore(BaseIFCBStore):
    """Readonly store for accessing IFCB ADC file objects."""

    def get(self, key):
        """Get the ADC file object for a specified bin."""
        data_dir = DataDirectory(self.data_dir)
        ifcb_bin = data_dir[key]
        return ifcb_bin.adc_file
