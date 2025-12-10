"""FastAPI entrypoint for a template stateless service."""

import os

from stateless_microservice import ServiceConfig, create_app

from .processor import MlAnalyzedProcessor

config = ServiceConfig(
    description="Template microservice framework.",
)

DATA_DIR = os.getenv("DATA_DIR", "/data/ifcb")

app = create_app(MlAnalyzedProcessor(data_dir=DATA_DIR), config)
