from abc import ABC, abstractmethod
from typing import Dict


class IEntityGenerator(ABC):
    """Abstract base class for entity generation and validation.

    This interface defines the structure for classes responsible for creating entities
    and validating data against entity schemas. Any class implementing this interface
    must define the `create` and `validate` methods.
    """
    @abstractmethod
    def create(self, entity_name: str, input_dict: Dict):
        """Abstract method for creating an entity from a schema.

         Args:
             entity_name (str): The name of the entity to be created.
             input_dict (Dict): A dictionary representing the schema of the entity.

         Raises:
             NotImplementedError: This method must be implemented in subclasses.
         """
        pass

    @abstractmethod
    def validate(self, entity_name: str, data: Dict):
        """Abstract method for validating data against an entity schema.

        Args:
            entity_name (str): The name of the entity schema to validate against.
            data (Dict): A dictionary containing the data to be validated.

        Raises:
            NotImplementedError: This method must be implemented in subclasses.
        """
        pass
