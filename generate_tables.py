# this is a temporary file 
# for generating the tables for testing
# later we will add migration files to do this

# initialize_db.py
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Import your Base and models
from adapters.wrap_orm_adapters.models.base import Base  # Importing the Base declarative instance
from adapters.wrap_orm_adapters.models.users import Users
from adapters.wrap_orm_adapters.models.organizations import Organizations
from adapters.wrap_orm_adapters.models.organization_users import OrganizationUsers


from adapters.wrap_orm_adapters.models.datasets import Datasets
from adapters.wrap_orm_adapters.models.files import Files
from adapters.wrap_orm_adapters.models.roles import Roles
from adapters.wrap_orm_adapters.models.studies import Studies
from adapters.wrap_orm_adapters.models.study_agreement_datasets import StudyAgreementDatasets
from adapters.wrap_orm_adapters.models.study_agreement_queries import StudyAgreementQueries
from adapters.wrap_orm_adapters.models.study_agreement_results import StudyAgreementResults
from adapters.wrap_orm_adapters.models.study_agreements import StudyAgreements
from adapters.wrap_orm_adapters.models.study_users import StudyUsers
from adapters.wrap_orm_adapters.models.user_roles import UserRoles

username = os.getenv("USERNAME")
password = os.getenv("PASSWORD")
database = os.getenv("DATABASE")
host = os.getenv("HOST")
port = os.getenv("DB_PORT")

# Create a SQLAlchemy engine
engine = create_engine(f'postgresql+psycopg2://{username}:{password}@{host}:{port}/{database}')

# Create tables
def initialize_database():
    print("Creating tables in the database...")
    
    base_class = Users.__bases__[0]
    # schema_mapper = get_schema_mapper()
    base_class.metadata.create_all(engine)
    print("All tables created successfully.")

if __name__ == "__main__":
    initialize_database()
