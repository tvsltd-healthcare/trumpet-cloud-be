import os

import bcrypt
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

from adapters.wrap_orm_adapters.models.users import Users
from adapters.wrap_orm_adapters.models.organizations import Organizations
from adapters.wrap_orm_adapters.models.organization_users import OrganizationUsers
from adapters.wrap_orm_adapters.models.roles import Roles
from adapters.wrap_orm_adapters.models.user_roles import UserRoles

from adapters.wrap_orm_adapters.models.datasets import Datasets
from adapters.wrap_orm_adapters.models.files import Files
from adapters.wrap_orm_adapters.models.studies import Studies
from adapters.wrap_orm_adapters.models.study_agreement_datasets import StudyAgreementDatasets
from adapters.wrap_orm_adapters.models.study_agreement_queries import StudyAgreementQueries
from adapters.wrap_orm_adapters.models.study_agreement_results import StudyAgreementResults
from adapters.wrap_orm_adapters.models.study_agreements import StudyAgreements
from adapters.wrap_orm_adapters.models.study_users import StudyUsers
from adapters.wrap_orm_adapters.models.organization_study_agreements import OrganizationStudyAgreements
from adapters.wrap_orm_adapters.models.notifications import Notifications

def insert_data(data, session):
    try:
        with session() as session:
            session.add_all(instances=data)
            session.commit()
            print("Data inserted successfully.")
    except Exception as e:
        print(f"Seed data insert error. {e}")


def reset_sequences(table_name: str, column_name: str, session):
    try:
        with session() as session:
            seq_name = f"{table_name}_{column_name}_seq"
            sql = text(f"SELECT setval('{seq_name}', (SELECT MAX(id) FROM {table_name}))")
            session.execute(sql)
            session.commit()
            print(f"Sequences: {seq_name}  reset successfully.")
    except Exception as e:
        print(f"Error resetting sequences: {e}")


def seed_database():
    username = os.getenv("DB_USERNAME")
    password = os.getenv("DB_PASSWORD")
    database = os.getenv("DB_NAME")
    host = os.getenv("DB_HOST")
    port = os.getenv("DB_PORT")
    admin_email = os.getenv("INITIAL_ADMIN_EMAIL", "admin@trumpetproject.eu")
    admin_phone = os.getenv("INITIAL_ADMIN_PHONE", "012345678901")
    admin_first_name = os.getenv("INITIAL_ADMIN_FIRST_NAME", "Trumpet")
    admin_last_name = os.getenv("INITIAL_ADMIN_LAST_NAME", "Admin")
    admin_address = os.getenv("INITIAL_ADMIN_ADDRESS", "Europe")

    user_password = bcrypt.hashpw(os.getenv("TRUMPET_ADMIN_PASSWORD").encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    engine = create_engine(f'postgresql+psycopg2://{username}:{password}@{host}:{port}/{database}')
    session = sessionmaker(bind=engine)

    insert_data(
        [
            Roles(name="trumpet_admin", id=1),
            Roles(name="researcher_admin", id=2),
            Roles(name="data_owner_admin", id=3),
            Roles(name="researcher", id=4)
        ],
        session
    )

    insert_data(
        [
            Organizations(id=1, name=admin_first_name, email=admin_email, address=admin_address, phone=admin_phone,
                          status="approved", type="governance"),
            Users(id=1, first_name=admin_first_name, last_name=admin_last_name, password=user_password,
                  email=admin_email,
                  phone=admin_phone, status="approved"),
            OrganizationUsers(organization_id=1, user_id=1),
            UserRoles(user_id=1, role_id=1), ],
        session)

    for table_name in ["roles", "organizations", "users"]:
        reset_sequences(table_name, "id", session)


if __name__ == "__main__":
    seed_database()
