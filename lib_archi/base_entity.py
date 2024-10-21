from abc import ABC, abstractmethod


class BaseEntity(ABC):
    """Abstract base class for all entities to enforce required attributes or methods."""

    @property
    @abstractmethod
    def id(self) -> str:
        """Every entity must have an id property"""
        pass
