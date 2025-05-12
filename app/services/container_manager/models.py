"""
Module for container manager models.
"""

# Imports from standard library
from dataclasses import dataclass, field
from typing import Optional, Dict, Any


@dataclass
class ContainerConfig:
    """
    Configuration for container.
    """

    image: str
    name: Optional[str] = None
    command: Optional[str] = None
    environment: Optional[Dict[str, Any]] = field(default_factory=dict)
    ports: Optional[Dict[str, Any]] = field(default_factory=dict)
    volumes: Optional[Dict[str, Any]] = field(default_factory=dict)
    restart_policy: Optional[str] = None
    detach: bool = True
    remove: bool = True
    tty: bool = False
    stdin_open: bool = False
