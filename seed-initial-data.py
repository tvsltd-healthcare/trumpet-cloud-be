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

def insert_data(data, session):
    try:
        with session() as session:
            session.add_all(instances=data)
            session.commit()
            print("Data inserted successfully.")
    except Exception as e:
        print(e)


def seed_database():
    username = os.getenv("DB_USERNAME")
    password = os.getenv("DB_PASSWORD")
    database = os.getenv("DB_NAME")
    host = os.getenv("DB_HOST")
    port = os.getenv("DB_PORT")

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
        [Organizations(id=1, name="system", email="admin@trumpetproject.eu", address="europe", phone="004400001",
                       status="approved", type="governance"),
         Users(id=1, first_name="trumpet", last_name="admin", password=user_password, email="admin@trumpetproject.eu",
               status="approved"), OrganizationUsers(organization_id=1, user_id=1), UserRoles(user_id=1, role_id=1), ],
        session)

    insert_data([Organizations(id=2, name="researcher-org-one", email="researcher-admin-one@researcher-one.org",
                               address="europe", phone="004400002", status="approved", type="researcher"),

                 Users(id=2, first_name="researcher-admin-one", last_name="researcher-org-one", password=user_password,
                       email="researcher-admin-one@researcher-one.org", status="approved"),
                 OrganizationUsers(organization_id=2, user_id=2), UserRoles(user_id=2, role_id=2),

                 Users(id=3, first_name="researcher-one", last_name="researcher-org-one", password=user_password,
                       email="researcher-one@researcher-one.org", status="approved"),
                 OrganizationUsers(organization_id=2, user_id=3), UserRoles(user_id=2, role_id=4), ], session)

    insert_data(
        [Organizations(id=3, name="do-org-one", email="do-admin-one@do-one.org", address="europe", phone="004400003",
                       status="approved", type="data_owner", host="https://trumpetdo1.technovativesolutions.co.uk"),

         Users(id=4, first_name="do-admin-one", last_name="do-org-one", password=user_password,
               email="do-admin-one@do-one.org", status="approved"), OrganizationUsers(organization_id=3, user_id=4),
         UserRoles(user_id=4, role_id=3), ], session)

    insert_data(
        [Organizations(id=4, name="do-org-two", email="do-admin-one@do-two.org", address="europe", phone="004400004",
                       status="approved", type="data_owner", host="https://trumpetdo2.technovativesolutions.co.uk"),
         Users(id=5, first_name="do-admin-one", last_name="do-org-two", password=user_password,
               email="do-admin-one@do-two.org", status="approved"), OrganizationUsers(organization_id=4, user_id=5),
         UserRoles(user_id=5, role_id=3), ], session)

    insert_data([Studies(id=1, name="Study one", description="Study one description", purpose="Study one purpose",
                         status="active", organization_id=2), ], session)

    insert_data(
        [StudyAgreements(id=1, study_id=1, status="approved", purpose="Study agreement one purpose", participants="3,4",
                         samples="1000", pet="None", model="NN_HNC", legal="Study agreement one legal",
                         study_privacy_budget="10000", created_by=3),
         OrganizationStudyAgreements(study_agreement_id=1, organization_id=2, organization_type="researcher",
                                     status="approved"),
         OrganizationStudyAgreements(study_agreement_id=1, organization_id=3, organization_type="data_owner",
                                     status="approved"),
         OrganizationStudyAgreements(study_agreement_id=1, organization_id=4, organization_type="data_owner",
                                     status="approved"), ], session)


if __name__ == "__main__":
    seed_database()
