from importlib.metadata import version

from .container_scheduler import ContainerScheduler, start

__version__ = version(__package__)
