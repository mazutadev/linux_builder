from .application import Application


__all__ = ["get_application"]


def get_application() -> Application:
    """
    Get the application instance.
    """

    return Application()
