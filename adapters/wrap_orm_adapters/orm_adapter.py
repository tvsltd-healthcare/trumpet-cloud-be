import os
import importlib

from typing import Dict, Any, List, Union

from application_layer.abstractions.orm_interface import IOrm
from wrap_orm import ORMWrapper

from adapters.wrap_orm_adapters.models import get_schema_mapper

import inflect

inflect_engine = inflect.engine()

class OrmAdapter(IOrm):
    """Adapter class for interacting with the ORM.

    This class provides methods for querying, inserting, updating, and deleting data
    using the ORMWrapper. It implements the IOrm interface.
    """

    MODEL_DIRECTORY = 'models'
    MODEL_PACKAGE_NAME = 'adapters.wrap_orm_adapters.models'
    WRAPPER_TYPE = 'sqlalchemy'
    
    def __init__(self, connection: object):
        """Initializes the ORM adapter with connection and schema mapping.

        Args:
            connection (object): The database connection object.
            db_type (str): The type of the database (e.g., MySQL, PostgreSQL).
            schema_mapper (dict): A dictionary for mapping schemas to entities.
        """
        schema_mapper = get_schema_mapper()
        self.orm_wrapper = ORMWrapper(connection, self.WRAPPER_TYPE, schema_mapper)

    def query(self, query_dict: Dict[str, Any]) -> List[object]:
        """Queries data from the database using the specified criteria.

        Args:
            query_dict (Dict[str, Any]): A dictionary representing the query criteria.

        Returns:
            List[object]: A list of objects that match the query criteria.
        """
        return self.orm_wrapper.query(query_dict)

    def insert(self, insert_query: Union[Dict[str, Any], List[Dict[str, Any]]]) -> List[object]:
        """Inserts data into the database.

        Args:
            insert_query (Union[Dict[str, Any], List[Dict[str, Any]]]): A dictionary or list of dictionaries
            representing the data to be inserted.

        Returns:
            List[object]: A list of objects that were inserted.
        """
        return self.orm_wrapper.insert(insert_query)

    def update(self, update_query: Dict[str, Any]) -> List[object]:
        """Updates data in the database.

        Args:
            update_query (Dict[str, Any]): A dictionary representing the update criteria and data.

        Returns:
            List[object]: A list of updated objects.
        """
        return self.orm_wrapper.update(update_query)

    def delete(self, delete_query: Dict[str, Any]) -> int:
        """Deletes data from the database.

        Args:
            delete_query (Dict[str, Any]): A dictionary representing the deletion criteria.

        Returns:
            int: The number of records deleted.
        """
        return self.orm_wrapper.delete(delete_query)
