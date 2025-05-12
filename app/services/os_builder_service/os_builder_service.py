"""
Module for OS builder service.
"""

# Imports from standard library
from typing import TYPE_CHECKING

# Imports from local modules
from .models import OSBuildConfig
from .exceptions import (
    OSBuildAlreadyExistsError,
)

# Imports from services modules
from app.services.container_manager import (
    ContainerManagerService,
    ContainerConfig,
)

if TYPE_CHECKING:

    # Imports from standard library
    import logging

    # Imports from third party libraries
    import docker


class OSBuilderService:
    """
    Service for building OS.
    """

    def __init__(
        self,
        logger: "logging.Logger",
        container_manager: "ContainerManagerService",
    ):
        self._logger = logger.getChild("OSBuilderService")
        self._container_manager = container_manager

        self._logger.info("OSBuilderService initialized")

    def build_os(self, parameters: OSBuildConfig) -> str:
        """
        Build an OS.
        """
        self._logger.info(
            "Building OS (name=%s, distro=%s, release=%s, architecture=%s, packages=%s)",
            parameters.name,
            parameters.distro,
            parameters.release,
            parameters.architecture,
            parameters.packages,
        )

        # Check if the OS already exists
        if self._container_manager.application_exists(parameters.name):
            raise OSBuildAlreadyExistsError(
                f"OS with name={parameters.name} already exists"
            )

        packages = " ".join(parameters.packages)

        # Build the OS
        self._container_manager.deploy_application(
            ContainerConfig(
                image=f"{parameters.distro}:{parameters.release}",
                name=parameters.name,
                command="sleep infinity",
                detach=True,
                remove=False,
                tty=True,
                stdin_open=True,
            )
        )

        return "OS built"
