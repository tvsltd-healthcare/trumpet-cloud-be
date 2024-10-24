# from .datasets import Datasets
# from .files import Files
# from .organization_users import OrganizationUsers
# from .organizations import Organizations
# from .roles import Roles
# from .studies import Studies
# from .study_agreement_datasets import StudyAgreementDatasets
# from .study_agreement_queries import StudyAgreementQueries
# from .study_agreement_results import StudyAgreementResults
# from .study_agreements import StudyAgreements
# from .study_users import StudyUsers
# from .user_roles import UserRoles
# from .users import Users

# __all__ = ['Datasets', 'Files', 'OrganizationUsers', 'Organizations', 'Roles', 'Studies', 'StudyAgreementDatasets', 'StudyAgreementQueries', 'StudyAgreementResults', 'StudyAgreements', 'StudyUsers', 'UserRoles', 'Users']

#temp
from sqlalchemy import create_engine
from dotenv import load_dotenv
load_dotenv()
from base import Base # temp
#temp end

import os
import importlib
from typing import Any, Dict
import stringcase
import inflect

# from sqlalchemy.orm import DeclarativeMeta

# Initialize the inflect engine for singularization
inflect_engine = inflect.engine()

current_dir = os.path.dirname(__file__)

def get_schema_mapper() -> Dict[str, Any]:
    """Dynamically loads classes from Python modules in the current directory and maps
    them using a snake_case singular form of the class name.

    This function dynamically imports Python modules in the current directory (excluding `__init__.py`)
    and extracts any class definitions. The class names are converted to snake_case and singularized
    before being added to the returned dictionary.

    Returns:
        Dict[str, Any]: A dictionary where the keys are the snake_case singular form of class names
        and the values are the class objects.
    """
    schema_mapper = {}

    for filename in os.listdir(current_dir):
        if filename.endswith('.py') and filename != '__init__.py':
            module_name = filename[:-3]
            module = importlib.import_module(f'.{module_name}', package=__name__)

            # print('creating table------')
            # print('creating table------')
            # print('creating table------')
            # Base.metadata.create_all(engine) # temp

            # Iterate through the attributes of the module
            for name, obj in vars(module).items():
                if isinstance(obj, type) and obj.__module__ == module.__name__ and not name.startswith('__'):
                    # Convert PascalCase class name to snake_case and singularize
                    key_name = pascal_plural_to_snake_singular(name)
                    
                    # Add the class to the dictionary with the snake_case singular name as the key
                    schema_mapper[key_name] = obj

    

    return schema_mapper


def pascal_plural_to_snake_singular(name: str) -> str:
    """Converts a PascalCase plural name to snake_case singular form."""
    # Convert PascalCase to snake_case
    snake_case_name = stringcase.snakecase(name)
    
    # Convert the plural form to singular
    singular_name = inflect_engine.singular_noun(snake_case_name) or snake_case_name
    
    return singular_name
