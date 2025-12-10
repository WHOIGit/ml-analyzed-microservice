"""Stateless template processor."""

import logging
from typing import List

from pydantic import BaseModel, Field

from stateless_microservice import BaseProcessor, StatelessAction, run_blocking

from ml_analyzed_service.bin_store import IFCBHeadersStore

from storage.utils import ReadonlyStore

logger = logging.getLogger(__name__)

class MlAnalyzedPathParams(BaseModel):
    """ Path parameters for the ml_analyzed analysis. """

    bin_id: str = Field(..., description="ID of bin to compute ml_analyzed for.")


class MlAnalyzedProcessor(BaseProcessor):
    """Processor for computing ml_analyzed."""

    def __init__(self, data_dir: str):
        header_store = ReadonlyStore(IFCBHeadersStore(data_dir))
        self.header_store = header_store

    @property
    def name(self) -> str:
        return "Ml-Analyzed Microservice"

    def get_stateless_actions(self) -> List[StatelessAction]:
        return [
            StatelessAction(
                name="echo",
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
        header = await run_blocking(self.header_store.get, bin_id)
        logger.info(f'Got header for {bin_id}: {header}')
        return "TODO"
