"""
Module for executing commands through subprocess.
"""

# Imports from standard library
import subprocess
import logging
from typing import List

# Imports from package
from .models import CommandResult
from .enums import CommandStatus


class CommandExecutor:
    """Class for executing commands through subprocess"""

    def __init__(self, logger: logging.Logger, timeout: int = 300):
        """
        Initialize command executor

        Args:
            timeout: Command execution timeout in seconds
        """
        self._logger = logger.getChild("CommandExecutor")
        self.timeout = timeout

    def _prepare_command(self, command: str, use_sudo: bool = False) -> List[str]:
        """
        Prepare command to execute

        Args:
            command: Command to execute

        Returns:
            List of command arguments
        """
        if use_sudo:
            return ["sudo"] + command.split()
        return command.split()

    def execute(self, command: str, use_sudo: bool = False) -> CommandResult:
        """
        Execute command

        Args:
            command: Command to execute

        Returns:
            Command result
        """
        try:
            process = subprocess.Popen(
                self._prepare_command(command, use_sudo),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )

            stdout, stderr = process.communicate(timeout=self.timeout)
            return_code = process.returncode

            status = CommandStatus.SUCCESS if return_code == 0 else CommandStatus.FAILED

            return CommandResult(
                status=status,
                stdout=stdout.strip(),
                stderr=stderr.strip(),
                return_code=return_code,
                command=command,
            )

        except subprocess.TimeoutExpired:
            process.kill()
            return CommandResult(
                status=CommandStatus.TIMEOUT,
                stdout="",
                stderr=f"Command timed out after {self.timeout} seconds",
                return_code=-1,
                command=command,
            )
        except Exception as e:
            return CommandResult(
                status=CommandStatus.FAILED,
                stdout="",
                stderr=str(e),
                return_code=-1,
                command=command,
            )

    def execute_with_prompt(self, command: str, prompt: str) -> CommandResult:
        """
        Execute command with prompt

        Args:
            command: Command to execute
            prompt: Prompt to expect

        Returns:
            Command result
        """
        try:
            process = subprocess.Popen(
                self._prepare_command(command),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                stdin=subprocess.PIPE,
                text=True,
            )

            stdout, stderr = process.communicate(
                input=prompt + "\n", timeout=self.timeout
            )
            return_code = process.returncode

            status = CommandStatus.SUCCESS if return_code == 0 else CommandStatus.FAILED

            return CommandResult(
                status=status,
                stdout=stdout.strip(),
                stderr=stderr.strip(),
                return_code=return_code,
                command=command,
            )

        except subprocess.TimeoutExpired:
            process.kill()
            return CommandResult(
                status=CommandStatus.TIMEOUT,
                stdout="",
                stderr=f"Command timed out after {self.timeout} seconds",
                return_code=-1,
                command=command,
            )
        except Exception as e:
            return CommandResult(
                status=CommandStatus.FAILED,
                stdout="",
                stderr=str(e),
                return_code=-1,
                command=command,
            )
