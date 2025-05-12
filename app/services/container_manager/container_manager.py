"""
Module for managing containers.
"""

# Imports from third party libraries
import logging

# Imports from local modules
from app.services.docker_service.docker_service import DockerService


class ContainerManagerService:
    """
    Service for managing containers.
    """

    def __init__(self, logger: logging.Logger, docker_service: DockerService):
        self._logger = logger.getChild("ContainerManagerService")
        self._docker_service = docker_service
