"""
Module for OS builder service exceptions.
"""


class OSBuildError(Exception):
    """
    Exception for OS build error.
    """


class OSBuildFailedError(OSBuildError):
    """
    Exception for OS build failed.
    """


class OSBuildTimeoutError(OSBuildError):
    """
    Exception for OS build timeout.
    """


class OSBuildCancelledError(OSBuildError):
    """
    Exception for OS build cancelled.
    """


class OSBuildAlreadyExistsError(OSBuildError):
    """
    Exception for OS build already exists.
    """


class OSBuildNotStartedError(OSBuildError):
    """
    Exception for OS build not started.
    """


# Distro config errors


class InvalidOSBuildConfigError(OSBuildError):
    """
    Exception for invalid OS build config.
    """


class OSBuildDistroNotSupportedError(InvalidOSBuildConfigError):
    """
    Exception for OS build distro not supported.
    """


class OSBuildReleaseNotSupportedError(InvalidOSBuildConfigError):
    """
    Exception for OS build release not supported.
    """


class OSBuildArchitectureNotSupportedError(InvalidOSBuildConfigError):
    """
    Exception for OS build architecture not supported.
    """
