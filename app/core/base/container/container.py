"""
Module for dependency injection container.
"""

# Imports from standard library
import os
from typing import TYPE_CHECKING

# Imports from third party libraries
from dependency_injector import containers, providers


if TYPE_CHECKING:

    # Imports from standard library
    import logging

    # Imports from core modules
    from app.core.base.commander import CommandExecutor

    # Imports from services modules
    from app.services.docker_service import DockerService
    from app.services.container_manager import ContainerManagerService
    from app.services.os_builder_service import OSBuilderService


def _find_project_root() -> str:
    """
    Find the project root directory.

    Returns:
        str: Absolute path to project root directory

    Raises:
        FileNotFoundError: If .root file is not found
        in any parent directory
    """
    current_dir = os.getcwd()

    while current_dir != os.path.dirname(current_dir):
        if ".root" in os.listdir(current_dir):
            return current_dir
        current_dir = os.path.dirname(current_dir)

    raise FileNotFoundError(
        "Project root directory not found. Make sure .root file "
        "exists in project root"
    )


def _init_logger(config: providers.Configuration) -> "logging.Logger":
    """
    Initialize logger.
    """

    from app.core.base.logger import get_logger, LogConfig

    # Register providers
    log_config = providers.Factory(
        LogConfig,
        level=config.logging.level,
        handlers=config.logging.handlers,
        file_config=config.logging.file_config,
        fmt=config.logging.format,
        datefmt=config.logging.datefmt,
        use_colors=config.logging.use_colors,
    )

    return providers.Singleton(get_logger, log_config)


def _init_commander(
    config: providers.Configuration, logger: providers.Singleton
) -> "CommandExecutor":
    """
    Initialize commander.
    """

    from app.core.base.commander import CommandExecutor

    return providers.Singleton(
        CommandExecutor,
        logger=logger,
        timeout=config.commander.timeout,
    )


def _init_docker_service(
    config: providers.Configuration,
    logger: providers.Singleton,
) -> "DockerService":
    """
    Initialize docker service.
    """

    from app.services.docker_service import DockerService, DockerServiceConfig

    # Docker service config
    docker_config = providers.Factory(
        DockerServiceConfig,
        base_url=config.docker.base_url,
        version=config.docker.version,
        timeout=config.docker.timeout,
    )

    return providers.Singleton(
        DockerService,
        logger=logger,
        configuration=docker_config,
    )


def _init_container_manager(
    logger: providers.Singleton,
    docker_service: providers.Singleton,
) -> "ContainerManagerService":
    """
    Initialize container manager.
    """

    from app.services.container_manager import ContainerManagerService

    return providers.Singleton(
        ContainerManagerService,
        logger=logger,
        docker_service=docker_service,
    )


def _init_os_builder(
    logger: providers.Singleton,
    container_manager: providers.Singleton,
) -> "OSBuilderService":
    """
    Initialize OS builder.
    """

    from app.services.os_builder_service import OSBuilderService

    return providers.Singleton(
        OSBuilderService,
        logger=logger,
        container_manager=container_manager,
    )


# Container
class Container(containers.DeclarativeContainer):
    """
    Base container for dependency injection.
    """

    # Find project root directory
    PROJECT_ROOT = providers.Singleton(_find_project_root)
    CONFIG_PATH = None

    # Configuration Provider
    config = providers.Configuration()

    # Logger Core
    logger = _init_logger(config)

    # Commander Core
    commander = _init_commander(config, logger)

    # Docker service
    docker_service = _init_docker_service(config, logger)

    # Container manager
    container_manager = _init_container_manager(logger, docker_service)

    # OS builder
    os_builder = _init_os_builder(logger, container_manager)
