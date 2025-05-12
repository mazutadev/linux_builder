"""
Module for managing containers.
"""

# Imports from standard library
from typing import TYPE_CHECKING, Optional

# Imports from local modules
from app.services.container_manager.models import ContainerConfig


if TYPE_CHECKING:

    # Imports from local modules
    from app.services.docker_service.docker_service import DockerService

    # Imports from third party libraries
    import logging
    import docker


class ContainerManagerService:
    """
    Service for managing containers.
    """

    def __init__(self, logger: "logging.Logger", docker_service: "DockerService"):
        self._logger = logger.getChild("ContainerManagerService")
        self._docker_service = docker_service

        self._logger.info("ContainerManagerService initialized")

    def deploy_application(
        self,
        parameters: ContainerConfig,
    ) -> Optional["docker.models.containers.Container"]:
        """
        Deploy an application.
        """
        self._logger.info(
            "Deploying application image=%s, parameters=%s",
            parameters.image,
            parameters,
        )

        container = None

        try:

            self._logger.info("Pulling image (image=%s)", parameters.image)
            self._docker_service.pull_image(parameters.image)

            self._logger.info("Running container (image=%s)", parameters.image)
            container = self._docker_service.run_container(
                image=parameters.image,
                name=parameters.name,
                command=parameters.command,
                environment=parameters.environment,
                ports=parameters.ports,
                volumes=parameters.volumes,
                restart_policy=parameters.restart_policy,
                detach=parameters.detach,
                remove=parameters.remove,
            )

        except Exception as e:
            self._logger.error("Error deploying application: %s", e)
            raise e

        return container

    def remove_application(
        self, container_id: str
    ) -> "docker.models.containers.Container":
        """
        Remove an application.
        """
        self._logger.info("Removing application (container_id=%s)", container_id)
        self._docker_service.stop_container(container_id)
        container = self._docker_service.remove_container(container_id)

        return container

    def application_exists(self, name: str) -> bool:
        """
        Check if an application exists.
        """
        return self._docker_service.container_exists(name)
