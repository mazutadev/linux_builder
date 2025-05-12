# Imports from standard library
import os
import logging
import threading
from pathlib import Path

# Imports from third party libraries
from dependency_injector import providers

# Imports from local modules
from app.core.base.container import Container
from app.core.base.commander import CommandExecutor

# Imports from services modules
from app.services.docker_service import DockerService


def _load_config_to_container(container: Container):
    """
    Load configuration from yaml files.
    """

    # Find config directory
    config_path = Path(container.PROJECT_ROOT()) / "config"
    container.CONFIG_PATH = providers.Object(config_path)

    def safe_load_config(config_provider: providers.Configuration, path: Path):
        if path.exists() and path.stat().st_size > 0:
            config_provider.from_yaml(path)

    # Load config from yaml file
    safe_load_config(container.config, config_path / "config.yaml")

    # Load config from environment variables
    env = os.getenv("APP_ENV", "development")
    safe_load_config(container.config, config_path / f"{env}_config.yaml")

    # Load local config if it exists
    safe_load_config(container.config, config_path / "local_config.yaml")


def init_container() -> Container:
    """
    Initialize dependency container.
    """

    container = Container()

    # Load config to container
    _load_config_to_container(container)

    return container


class Application:
    """
    Base class for main applications.
    """

    _instance: "Application" = None
    _lock: threading.Lock = threading.Lock()

    # Singleton pattern
    def __new__(cls, *args, **kwargs):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls, *args, **kwargs)
                cls._instance._initialized = False

            return cls._instance

    def __init__(self):
        if self._initialized:
            return

        # Initialize container
        self._container = init_container()
        self.__inner_logger = self._container.logger().getChild("CoreApplication init")

        self.__inner_logger.debug("Initializing CoreApplication")

        self.__inner_logger.debug(
            "Root project path: %s", self._container.PROJECT_ROOT()
        )

        self.__inner_logger.debug("Config path: %s", self._container.CONFIG_PATH())
        self.__inner_logger.debug("Config loaded: %s", self._container.config())

        # Initialize logger
        self._logger = self._container.logger()
        self.__inner_logger.debug("Logger initialized")

        # Initialize Commander
        self._commander = self._container.commander()
        self.__inner_logger.debug("Commander initialized")

        # Initialize Docker service
        self._docker_service = self._container.docker_service()
        self.__inner_logger.debug("Docker service initialized")

        # Set initialized flag
        self._initialized = True
        self.__inner_logger.debug("CoreApplication initialized")

    @classmethod
    def _initialized(cls) -> bool:
        return cls._initialized

    @property
    def container(self) -> Container:
        return self._container

    @property
    def logger(self) -> logging.Logger:
        return self._logger

    @property
    def commander(self) -> CommandExecutor:
        return self._commander

    @property
    def docker_service(self) -> DockerService:
        return self._docker_service
