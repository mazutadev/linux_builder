"""
Module for OS builder service models.
"""

# imports from standard library
from dataclasses import dataclass
from typing import List

# imports from local modules exceptions
from app.services.os_builder_service.exceptions import (
    OSBuildDistroNotSupportedError,
    OSBuildReleaseNotSupportedError,
    OSBuildArchitectureNotSupportedError,
)


@dataclass
class OSBuildConfig:
    """
    Configuration for OS build.
    """

    name: str
    distro: str
    release: str
    architecture: str
    packages: List[str]

    def __post_init__(self):
        if self.distro not in ["ubuntu", "debian"]:
            raise OSBuildDistroNotSupportedError(f"Distro {self.distro} not supported")

        if self.release not in ["20.04", "22.04", "24.04", "latest"]:
            raise OSBuildReleaseNotSupportedError(
                f"Release {self.release} not supported"
            )

        if self.architecture not in ["amd64", "arm64"]:
            raise OSBuildArchitectureNotSupportedError(
                f"Architecture {self.architecture} not supported"
            )
