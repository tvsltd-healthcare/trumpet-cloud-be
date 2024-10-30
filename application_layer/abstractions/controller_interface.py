from abc import ABC, abstractmethod
from typing import Optional


class IController(ABC):
    """Abstract base class for handling CRUD operations on entities.

    This interface defines the structure for classes responsible for creating,
    retrieving, updating, and deleting entities, as well as handling collections of entities.
    Implementing classes must define methods for each CRUD operation.
    """
    
    @abstractmethod
    def post(self, entity: object, request: object) -> Optional[object]:
        """Abstract method for creating a new entity.

         Args:
             entity (object): The entity object containing data for creation.
             request (object): Additional request context or parameters.

         Returns:
             Optional[object]: The created entity object, or None if creation fails.

         Raises:
             NotImplementedError: This method must be implemented in subclasses.
         """
        pass

    @abstractmethod
    def get(self, request: object) -> object:
        """Abstract method for retrieving a single entity.

        Args:
            request (object): Additional request context or parameters for retrieval.

        Returns:
            object: The retrieved entity object.

        Raises:
            NotImplementedError: This method must be implemented in subclasses.
        """
        pass

    @abstractmethod
    def get_collection(self, request: object) -> object:
        """Abstract method for retrieving a collection of entities.

        Args:
            request (object): Additional request context or parameters for collection retrieval.

        Returns:
            object: A collection of entity objects.

        Raises:
            NotImplementedError: This method must be implemented in subclasses.
        """
        pass

    @abstractmethod
    def patch(self, entity: object, request: object) -> Optional[object]:
        """Abstract method for partially updating an existing entity.

        Args:
            entity (object): The entity object with fields to be updated.
            request (object): Additional request context or parameters.

        Returns:
            Optional[object]: The updated entity object, or None if the update fails.

        Raises:
            NotImplementedError: This method must be implemented in subclasses.
        """
        pass

    @abstractmethod
    def put(self, entity: object, request: object) -> Optional[object]:
        """Abstract method for fully replacing an existing entity.

        Args:
            entity (object): The entity object with full data for replacement.
            request (object): Additional request context or parameters.

        Returns:
            Optional[object]: The updated entity object, or None if the replacement fails.

        Raises:
            NotImplementedError: This method must be implemented in subclasses.
        """
        pass

    @abstractmethod
    def delete(self, request: object) -> Optional[object]:
        """Abstract method for deleting an existing entity.

        Args:
            request (object): Additional request context or parameters for deletion.

        Returns:
            Optional[object]: A confirmation of deletion or None if deletion fails.

        Raises:
            NotImplementedError: This method must be implemented in subclasses.
        """
        pass
