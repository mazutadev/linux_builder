"""
Module for working with Docker.
"""

# Imports from third party libraries

import docker
import logging
from typing import List

import docker.errors


# Imports from local modules
from app.services.docker_service.models import DockerServiceConfig


class DockerService:
    """
    Service for working with Docker.
    """

    def __init__(self, logger: logging.Logger, configuration: DockerServiceConfig):
        self._logger = logger.getChild("DockerService")
        self._configuration = configuration

        self._logger.debug("DockerServiceConfig: %s", self._configuration)

        self._logger.info("Initializing DockerService")

        self._client = docker.DockerClient(
            base_url=self._configuration.base_url,
            version=self._configuration.version,
            timeout=self._configuration.timeout,
        )

        self._logger.info("Docker client initialized")

    def list_containers(
        self, all: bool = True
    ) -> List[docker.models.containers.Container]:
        """
        List all containers.
        """
        try:
            self._logger.debug("Listing containers (all=%s)", all)
            return self._client.containers.list(all=all)
        except docker.errors.DockerException as e:
            self._logger.error("Error listing containers: %s", e)
            raise e

    def run_container(
        self, image: str, command: str = None, **kwargs
    ) -> docker.models.containers.Container:
        """
        Run a container.
        """
        try:
            self._logger.info(
                "Running container (image=%s, command=%s)", image, command
            )
            return self._client.containers.run(image, command, detach=True, **kwargs)
        except docker.errors.DockerException as e:
            self._logger.error("Error running container: %s", e)
            raise e

    def stop_container(self, container_id: str) -> docker.models.containers.Container:
        """
        Stop a container.
        """
        try:
            self._logger.debug("Stopping container (container_id=%s)", container_id)
            container = self._client.containers.get(container_id)
            container.stop()
            return container
        except docker.errors.DockerException as e:
            self._logger.error("Error stopping container: %s", e)
            raise e

    def remove_container(
        self, container_id: str, force: bool = False
    ) -> docker.models.containers.Container:
        """
        Remove a container.
        """
        try:
            self._logger.debug(
                "Removing container (container_id=%s, force=%s)", container_id, force
            )
            container = self._client.containers.get(container_id)
            container.remove(force=force)
            return container
        except docker.errors.DockerException as e:
            self._logger.error("Error removing container: %s", e)
            raise e

    def get_logs(self, container_id: str, tail: int = 100) -> str:
        """
        Get logs from a container.
        """
        try:
            self._logger.debug(
                "Getting logs from container (container_id=%s, tail=%s)",
                container_id,
                tail,
            )
            container = self._client.containers.get(container_id)
            logs = container.logs(tail=tail)
            return logs.decode()
        except docker.errors.DockerException as e:
            self._logger.error("Error getting logs from container: %s", e)
            raise e

    def pull_image(self, image: str) -> docker.models.images.Image:
        """
        Pull an image.
        """
        try:
            self._logger.debug("Pulling image (image=%s)", image)
            return self._client.images.pull(image)
        except docker.errors.DockerException as e:
            self._logger.error("Error pulling image: %s", e)
            raise e

    def build_image(self, path: str, tag: str) -> docker.models.images.Image:
        """
        Build an image.
        """
        try:
            self._logger.debug("Building image (path=%s, tag=%s)", path, tag)
            return self._client.images.build(path=path, tag=tag)
        except docker.errors.DockerException as e:
            self._logger.error("Error building image: %s", e)
            raise e
