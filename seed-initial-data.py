# seed_user.py

import os

import bcrypt
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

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
from adapters.wrap_orm_adapters.models.organization_study_agreements import OrganizationStudyAgreements

def seed_database():
    username = os.getenv("DB_USERNAME")
    password = os.getenv("DB_PASSWORD")
    database = os.getenv("DB_NAME")
    host = os.getenv("DB_HOST")
    port = os.getenv("DB_PORT")

    user_password = bcrypt.hashpw(os.getenv("TRUMPET_ADMIN_PASSWORD").encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    engine = create_engine(f'postgresql+psycopg2://{username}:{password}@{host}:{port}/{database}')
    Session = sessionmaker(bind=engine)

    # 1 | trumpet_admin | 2025 - 05 - 06
    # 14: 37:38.645 | 2025 - 05 - 06
    # 14: 37:38.645 | |
    # 3 | researcher_admin | 2025 - 05 - 06
    # 14: 37:38.645 | 2025 - 05 - 06
    # 14: 37:38.645 | |
    # 4 | data_owner_admin | 2025 - 05 - 06
    # 14: 37:38.645 | 2025 - 05 - 06
    # 14: 37:38.645 | |
    # 5 | researcher

    # 1 | system | admin @ trumpetproject.eu | europe | 123456789 | | | | 2025 - 05 - 06
    # 14: 37:38.645 | 2025 - 05 - 06
    # 14: 37:38.645 |
    #
    # |

    with Session() as session:
        session.add_all(instances=[
            Roles(name="trumpet_admin", id=1),
            Roles(name="researcher_admin", id=2),
            Roles(name="data_owner_admin", id=3),
            Roles(name="researcher", id=4)
        ])

        session.add_all(instances=[
            Organizations(id=1, name="system", email="admin@trumpetproject.eu", address="europe", phone="004400001",
                          status="approved", type="governance"),
            Users(id=1, first_name="trumpet", last_name="admin", password=user_password,
                  email="admin@trumpetproject.eu", status="approved"),
            OrganizationUsers(organization_id=1, user_id=1),
            UserRoles(user_id=1, role_id=1),
        ])

        session.add_all(instances=[
            Organizations(id=2, name="researcher-org-one", email="researcher-admin-one@researcher-one.org", address="europe",
                          phone="004400002", status="approved", type="researcher"),

            Users(id=2, first_name="researcher-admin-one", last_name="researcher-org-one", password=user_password,
                  email="researcher-admin-one@researcher-one.org", status="approved"),
            OrganizationUsers(organization_id=2, user_id=2),
            UserRoles(user_id=2, role_id=2),

            Users(id=3, first_name="researcher-one", last_name="researcher-org-one", password=user_password,
                  email="researcher-one@researcher-one.org", status="approved"),
            OrganizationUsers(organization_id=2, user_id=3),
            UserRoles(user_id=2, role_id=4),
        ])

        session.add_all(instances=[
            Organizations(id=3, name="do-org-one", email="do-admin-one@do-one.org",
                          address="europe",
                          phone="004400003", status="approved", type="data_owner"),

            Users(id=4, first_name="do-admin-one", last_name="do-org-one", password=user_password,
                  email="do-admin-one@do-one.org", status="approved"),
            OrganizationUsers(organization_id=3, user_id=4),
            UserRoles(user_id=4, role_id=3),
        ])

        session.add_all(instances=[
            Organizations(id=4, name="do-org-two", email="do-admin-one@do-two.org",
                          address="europe",
                          phone="004400004", status="approved", type="data_owner"),

            Users(id=5, first_name="do-admin-one", last_name="do-org-two", password=user_password,
                  email="do-admin-one@do-two.org", status="approved"),
            OrganizationUsers(organization_id=4, user_id=5),
            UserRoles(user_id=5, role_id=3),
        ])

        session.commit()


if __name__ == "__main__":
    seed_database()
