from abc import ABC, abstractmethod
from typing import Dict, Any, List, Union


class IOrm(ABC):
    """Abstract base class for interacting with the ORM.

    This interface defines the structure for ORM-related operations such as querying,
    inserting, updating, and deleting data. Any class implementing this interface
    must define these methods for interacting with the database.
    """

    @abstractmethod
    def query(self, query_dict: Dict[str, Any]) -> List[object]:
        """Abstract method for querying data from the database.

        Args:
            query_dict (Dict[str, Any]): A dictionary representing the query criteria.

        Returns:
            List[object]: A list of objects that match the query criteria.

        Raises:
            NotImplementedError: This method must be implemented in subclasses.
        """
        pass

    @abstractmethod
    def insert(self, insert_query: Union[Dict[str, Any], List[Dict[str, Any]]]) -> List[object]:
        """Abstract method for inserting data into the database.

        Args:
            insert_query (Union[Dict[str, Any], List[Dict[str, Any]]]): A dictionary or list of dictionaries
            representing the data to be inserted.

        Returns:
            List[object]: A list of objects that were inserted.

        Raises:
            NotImplementedError: This method must be implemented in subclasses.
        """
        pass

    @abstractmethod
    def update(self, update_query: Dict[str, Any]) -> List[object]:
        """Abstract method for updating data in the database.

        Args:
            update_query (Dict[str, Any]): A dictionary representing the update criteria and data.

        Returns:
            List[object]: A list of updated objects.

        Raises:
            NotImplementedError: This method must be implemented in subclasses.
        """
        pass

    @abstractmethod
    def delete(self, delete_query: Dict[str, Any]) -> int:
        """Abstract method for deleting data from the database.

        Args:
            delete_query (Dict[str, Any]): A dictionary representing the deletion criteria.

        Returns:
            int: The number of records deleted.

        Raises:
            NotImplementedError: This method must be implemented in subclasses.
        """
        pass
