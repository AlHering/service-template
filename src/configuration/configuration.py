# -*- coding: utf-8 -*-
"""
****************************************************
*          Basic Language Model Backend            *
*            (c) 2023 Alexander Hering             *
****************************************************
"""
import os
import logging
from dotenv import dotenv_values
from . import paths as PATHS


"""
Environment file
"""
ENV_PATH = os.path.join(PATHS.PACKAGE_PATH, ".env")
ENV = dotenv_values(ENV_PATH) if os.path.exists(ENV_PATH) else {}


"""
Logger
"""
LOGGER = logging.Logger("[ServiceServer]")


"""
Project information
"""
PROJECT_NAME = "Service server"
PROJECT_DESCRIPTION = "A server for providing services."
PROJECT_VERSION = "v0.1.0"


"""
Network addresses and interfaces
"""
BACKEND_HOST = ENV.get("BACKEND_HOST", "127.0.0.1")
BACKEND_PORT = int(ENV.get("BACKEND_PORT", "7861"))
BACKEND_TITLE =  "Service Backend"
BACKEND_DESCRIPTION = "Backend interface for the service server."
BACKEND_VERSION = PROJECT_VERSION
BACKEND_ENDPOINT_BASE = "/api/v1"


"""
Components
"""
DEFAULT_SERVICES = {
}


"""
Others
"""
FILE_UPLOAD_CHUNK_SIZE = 1024*1024
FILE_OUTPUT_CHUNK_SIZE = 1024