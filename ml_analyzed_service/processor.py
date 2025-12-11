"""ML analyzed processor for IFCB bins."""

import logging
from typing import List

from pydantic import BaseModel, Field

from stateless_microservice import BaseProcessor, StatelessAction, run_blocking

from ml_analyzed_service.bin_store import IFCBHeadersStore, IFCBADCFileStore

from storage.utils import ReadonlyStore

from ifcb.metrics.ml_analyzed import compute_ml_analyzed

logger = logging.getLogger(__name__)

class MlAnalyzedPathParams(BaseModel):
    """ Path parameters for the ml_analyzed analysis. """

    bin_id: str = Field(..., description="ID of bin to compute ml_analyzed for.")


class MinimalBin:
    """Lightweight bin wrapper for ml_analyzed computation without ROIs."""
    def __init__(self, adc_file, headers_dict):
        self.adc_file = adc_file
        self.headers_dict = headers_dict

    def header(self, key):
        """Access header values by key (case-insensitive)."""
        # Simple case-insensitive lookup
        key_lower = key.lower()
        for k, v in self.headers_dict.items():
            if k.lower() == key_lower:
                return v
        raise KeyError(f"Header key '{key}' not found")

    @property
    def adc(self):
        """The bin's ADC data as a pandas DataFrame."""
        return self.adc_file.csv


class MlAnalyzedProcessor(BaseProcessor):
    """Processor for computing ml_analyzed."""

    def __init__(self, data_dir: str):
        self.data_dir = data_dir
        header_store = ReadonlyStore(IFCBHeadersStore(data_dir))
        adc_file_store = ReadonlyStore(IFCBADCFileStore(data_dir))
        self.header_store = header_store
        self.adc_file_store = adc_file_store

    @property
    def name(self) -> str:
        return "Ml-Analyzed Microservice"

    def get_stateless_actions(self) -> List[StatelessAction]:
        return [
            StatelessAction(
                name="ml_analyzed",
                path="/ml_analyzed/{bin_id}",
                path_params_model=MlAnalyzedPathParams,
                handler=self.handle_ml_analyzed,
                summary="Compute ml analyze for the given bin.",
                description="Compute ml analyze for the given bin.",
                tags=("ifcb","ml_analyzed",),
                methods=("GET",),
                media_type="text/plain",
            ),
        ]

    async def handle_ml_analyzed(self, path_params: MlAnalyzedPathParams):
        """ Return ml_analyzed for the given payload. """

        bin_id = path_params.bin_id

        # Fetch lightweight data from stores
        adc_file = await run_blocking(self.adc_file_store.get, bin_id)
        headers = await run_blocking(self.header_store.get, bin_id)

        # Create minimal wrapper and compute
        bin_wrapper = MinimalBin(adc_file=adc_file, headers_dict=headers)
        ml_analyzed_value, _, _ = compute_ml_analyzed(bin_wrapper)

        logger.info(f'Computed ml_analyzed for {bin_id}: {ml_analyzed_value}')
        return str(ml_analyzed_value)
