"""FastAPI entrypoint for the ml_analyzed microservice."""

import os

from stateless_microservice import ServiceConfig, create_app

from .processor import MlAnalyzedProcessor

config = ServiceConfig(
    description="Microservice for computing ml_analyzed metric for IFCB bins.",
)

DATA_DIR = os.getenv("DATA_DIR", "/data/ifcb")

app = create_app(MlAnalyzedProcessor(data_dir=DATA_DIR), config)
