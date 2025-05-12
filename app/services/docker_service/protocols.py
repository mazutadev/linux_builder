"""
Module for Docker service protocols.
"""

# Imports from standard library
from typing import Protocol


class DockerServiceConfigProtocol(Protocol):
    """
    Protocol for Docker service.
    """

    base_url: str
    version: str
    timeout: int
