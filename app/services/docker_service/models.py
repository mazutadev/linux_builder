"""
Module for Docker service models.
"""

# Imports from standard library
from dataclasses import dataclass


@dataclass
class DockerServiceConfig:
    """
    Configuration for Docker service.
    """

    base_url: str
    version: str
    timeout: int
