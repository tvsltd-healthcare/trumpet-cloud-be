import os

import bcrypt
from sqlalchemy import create_engine, text
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

    insert_data([Datasets(
                        id=1,
                        don_uid="fe6a52fb-0520-4bb8-8a2f-bb9ae1ef0c41",
                        organization_id=3,
                        title="Head and neck cancer",
                        about="Head and neck cancer, DON one.",
                        use_case="HNC",
                        status="published",
                        temporal_coverage_start="2025-01-01 00:00:00",
                        temporal_coverage_end="2025-12-31 00:00:00",
                        geospatial_coverage="Spain",
                        doi_citation="Demo DOI 123",
                        provenance="European Union, Horizon 2020",
                        license_title="CC BY-NC-SA 4.0",
                        license_details="Creative Commons public licenses provide a standard set of terms and conditions that creators and other rights holders may use to share original works of authorship and other material subject to copyright and certain other rights specified in the public license below. The following considerations are for informational purposes only, are not exhaustive, and do not form part of our licenses.",
                        statistics='[{"key": "SUBJECT", "type": "object", "validity_count": {"valid": 2505, "missing": 0}}, {"key": "GENDER", "type": "object", "validity_count": {"valid": 2505, "missing": 0}}, {"key": "BIRTH_DATE", "type": "object", "validity_count": {"valid": 2505, "missing": 0}}, {"key": "DEATH_DATE", "type": "object", "validity_count": {"valid": 999, "missing": 1506}}, {"key": "OIS_PLAN_DATE", "type": "object", "validity_count": {"valid": 2505, "missing": 0}}, {"key": "TOPOLOGY", "type": "object", "validity_count": {"valid": 2505, "missing": 0}}, {"key": "HISTOLOGY", "type": "object", "validity_count": {"valid": 2437, "missing": 68}}, {"key": "T_CATEGORY", "type": "object", "validity_count": {"valid": 2505, "missing": 0}}, {"key": "N_CATEGORY", "type": "object", "validity_count": {"valid": 2505, "missing": 0}}, {"key": "M_CATEGORY", "type": "object", "validity_count": {"valid": 2505, "missing": 0}}, {"key": "OIS_TOTAL_DOSE", "type": "int64", "histogram": {"counts": [61, 81, 75, 78, 80, 198, 207, 263, 584, 878], "bin_labels": ["802.00 - 1421.80", "1421.80 - 2041.60", "2041.60 - 2661.40", "2661.40 - 3281.20", "3281.20 - 3901.00", "3901.00 - 4520.80", "4520.80 - 5140.60", "5140.60 - 5760.40", "5760.40 - 6380.20", "6380.20 - 7000.00"]}, "stat_summary": {"25%": 4711.0, "50%": 6110.0, "75%": 6575.0, "max": 7000.0, "min": 802.0, "std": 1524.9517668042822, "mean": 5450.534530938124, "count": 2505.0}, "validity_count": {"valid": 2505, "missing": 0}}, {"key": "OIS_NB_FRACTIONS", "type": "int64", "histogram": {"counts": [125, 114, 146, 101, 83, 133, 111, 484, 640, 568], "bin_labels": ["1.00 - 4.40", "4.40 - 7.80", "7.80 - 11.20", "11.20 - 14.60", "14.60 - 18.00", "18.00 - 21.40", "21.40 - 24.80", "24.80 - 28.20", "28.20 - 31.60", "31.60 - 35.00"]}, "stat_summary": {"25%": 19.0, "50%": 28.0, "75%": 31.0, "max": 35.0, "min": 1.0, "std": 9.411435464191216, "mean": 24.430339321357284, "count": 2505.0}, "validity_count": {"valid": 2505, "missing": 0}}, {"key": "ENT_VISIT_DATE", "type": "object", "validity_count": {"valid": 2505, "missing": 0}}, {"key": "WEIGHT", "type": "int64", "histogram": {"counts": [280, 255, 248, 229, 249, 263, 255, 219, 259, 248], "bin_labels": ["38.00 - 47.10", "47.10 - 56.20", "56.20 - 65.30", "65.30 - 74.40", "74.40 - 83.50", "83.50 - 92.60", "92.60 - 101.70", "101.70 - 110.80", "110.80 - 119.90", "119.90 - 129.00"]}, "stat_summary": {"25%": 60.0, "50%": 83.0, "75%": 106.0, "max": 129.0, "min": 38.0, "std": 26.420945121620417, "mean": 82.9812375249501, "count": 2505.0}, "validity_count": {"valid": 2505, "missing": 0}}, {"key": "HEIGHT", "type": "int64", "histogram": {"counts": [311, 241, 196, 250, 240, 288, 223, 258, 220, 278], "bin_labels": ["148.00 - 152.20", "152.20 - 156.40", "156.40 - 160.60", "160.60 - 164.80", "164.80 - 169.00", "169.00 - 173.20", "173.20 - 177.40", "177.40 - 181.60", "181.60 - 185.80", "185.80 - 190.00"]}, "stat_summary": {"25%": 158.0, "50%": 169.0, "75%": 180.0, "max": 190.0, "min": 148.0, "std": 12.3930447216539, "mean": 168.76127744510978, "count": 2505.0}, "validity_count": {"valid": 2505, "missing": 0}}, {"key": "BMI", "type": "float64", "histogram": {"counts": [198, 341, 374, 383, 365, 365, 248, 123, 80, 28], "bin_labels": ["10.60 - 15.35", "15.35 - 20.10", "20.10 - 24.85", "24.85 - 29.60", "29.60 - 34.35", "34.35 - 39.10", "39.10 - 43.85", "43.85 - 48.60", "48.60 - 53.35", "53.35 - 58.10"]}, "stat_summary": {"25%": 21.1, "50%": 29.0, "75%": 36.7, "max": 58.1, "min": 10.6, "std": 10.290174960764968, "mean": 29.56263473053892, "count": 2505.0}, "validity_count": {"valid": 2505, "missing": 0}}, {"key": "ECOG", "type": "int64", "histogram": {"counts": [581, 0, 568, 0, 0, 787, 0, 309, 0, 260], "bin_labels": ["0.00 - 0.40", "0.40 - 0.80", "0.80 - 1.20", "1.20 - 1.60", "1.60 - 2.00", "2.00 - 2.40", "2.40 - 2.80", "2.80 - 3.20", "3.20 - 3.60", "3.60 - 4.00"]}, "stat_summary": {"25%": 1.0, "50%": 2.0, "75%": 2.0, "max": 4.0, "min": 0.0, "std": 1.250707107429502, "mean": 1.6403193612774452, "count": 2505.0}, "validity_count": {"valid": 2505, "missing": 0}}, {"key": "GASTRIC_TUBE", "type": "bool", "validity_count": {"valid": 2505, "missing": 0}}, {"key": "TOBACCO_DATE", "type": "object", "validity_count": {"valid": 2505, "missing": 0}}, {"key": "NECRO_JAW", "type": "float64", "histogram": {"counts": [1892, 0, 140, 0, 0, 97, 0, 80, 0, 25], "bin_labels": ["0.00 - 0.40", "0.40 - 0.80", "0.80 - 1.20", "1.20 - 1.60", "1.60 - 2.00", "2.00 - 2.40", "2.40 - 2.80", "2.80 - 3.20", "3.20 - 3.60", "3.60 - 4.00"]}, "stat_summary": {"25%": 0.0, "50%": 0.0, "75%": 0.0, "max": 4.0, "min": 0.0, "std": 0.8043359702288315, "mean": 0.3017009847806625, "count": 2234.0}, "validity_count": {"valid": 2234, "missing": 271}}, {"key": "ORAL_MUCOSITIS", "type": "float64", "histogram": {"counts": [395, 0, 0, 378, 0, 0, 681, 0, 0, 924], "bin_labels": ["0.00 - 0.30", "0.30 - 0.60", "0.60 - 0.90", "0.90 - 1.20", "1.20 - 1.50", "1.50 - 1.80", "1.80 - 2.10", "2.10 - 2.40", "2.40 - 2.70", "2.70 - 3.00"]}, "stat_summary": {"25%": 1.0, "50%": 2.0, "75%": 3.0, "max": 3.0, "min": 0.0, "std": 1.0963211199105698, "mean": 1.8973927670311186, "count": 2378.0}, "validity_count": {"valid": 2378, "missing": 127}}, {"key": "DYSPHAGIA", "type": "float64", "histogram": {"counts": [250, 0, 0, 501, 0, 0, 805, 0, 0, 781], "bin_labels": ["0.00 - 0.30", "0.30 - 0.60", "0.60 - 0.90", "0.90 - 1.20", "1.20 - 1.50", "1.50 - 1.80", "1.80 - 2.10", "2.10 - 2.40", "2.40 - 2.70", "2.70 - 3.00"]}, "stat_summary": {"25%": 1.0, "50%": 2.0, "75%": 3.0, "max": 3.0, "min": 0.0, "std": 0.9838789792111691, "mean": 1.905862216516902, "count": 2337.0}, "validity_count": {"valid": 2337, "missing": 168}}, {"key": "CHEMOTHERAPY", "type": "object", "validity_count": {"valid": 1210, "missing": 1295}}, {"key": "SMOKING_CIGARETTE_QUANTITY", "type": "float64", "histogram": {"counts": [106, 44, 56, 44, 39, 55, 80, 77, 82, 178], "bin_labels": ["1.00 - 2.10", "2.10 - 3.20", "3.20 - 4.30", "4.30 - 5.40", "5.40 - 6.50", "6.50 - 7.60", "7.60 - 8.70", "8.70 - 9.80", "9.80 - 10.90", "10.90 - 12.00"]}, "stat_summary": {"25%": 4.0, "50%": 8.0, "75%": 10.0, "max": 12.0, "min": 1.0, "std": 3.4874375639077844, "mean": 7.298291721419186, "count": 761.0}, "validity_count": {"valid": 761, "missing": 1744}}]'
                )],
            session)

    insert_data([Datasets(
                        id=2,
                        don_uid="11f729da-d89b-4a48-929c-d81d01bf1bbb",
                        organization_id=4,
                        title="Head and neck cancer",
                        about="Head and neck cancer, DON two.",
                        use_case="HNC",
                        status="published",
                        temporal_coverage_start="2025-01-01 00:00:00",
                        temporal_coverage_end="2025-12-31 00:00:00",
                        geospatial_coverage="France",
                        doi_citation="Demo DOI 124",
                        provenance="European Union, Horizon 2020",
                        license_title="CC BY-NC-SA 4.0",
                        license_details="Creative Commons public licenses provide a standard set of terms and conditions that creators and other rights holders may use to share original works of authorship and other material subject to copyright and certain other rights specified in the public license below. The following considerations are for informational purposes only, are not exhaustive, and do not form part of our licenses.",
                        statistics='[{"key": "SUBJECT", "type": "object", "validity_count": {"valid": 2505, "missing": 0}}, {"key": "GENDER", "type": "object", "validity_count": {"valid": 2505, "missing": 0}}, {"key": "BIRTH_DATE", "type": "object", "validity_count": {"valid": 2505, "missing": 0}}, {"key": "OIS_PLAN_DATE", "type": "object", "validity_count": {"valid": 2505, "missing": 0}}, {"key": "TOPOLOGY", "type": "object", "validity_count": {"valid": 2505, "missing": 0}}, {"key": "HISTOLOGY", "type": "object", "validity_count": {"valid": 2427, "missing": 78}}, {"key": "CHEMOTHERAPY", "type": "object", "validity_count": {"valid": 1240, "missing": 1265}}, {"key": "T_CATEGORY", "type": "object", "validity_count": {"valid": 2505, "missing": 0}}, {"key": "N_CATEGORY", "type": "object", "validity_count": {"valid": 2505, "missing": 0}}, {"key": "M_CATEGORY", "type": "object", "validity_count": {"valid": 2505, "missing": 0}}, {"key": "OIS_TOTAL_DOSE", "type": "int64", "histogram": {"counts": [77, 55, 70, 72, 79, 216, 229, 232, 564, 911], "bin_labels": ["802.00 - 1421.80", "1421.80 - 2041.60", "2041.60 - 2661.40", "2661.40 - 3281.20", "3281.20 - 3901.00", "3901.00 - 4520.80", "4520.80 - 5140.60", "5140.60 - 5760.40", "5760.40 - 6380.20", "6380.20 - 7000.00"]}, "stat_summary": {"25%": 4657.0, "50%": 6119.0, "75%": 6588.0, "max": 7000.0, "min": 802.0, "std": 1522.697031243679, "mean": 5469.417964071857, "count": 2505.0}, "validity_count": {"valid": 2505, "missing": 0}}, {"key": "OIS_NB_FRACTIONS", "type": "int64", "histogram": {"counts": [145, 108, 135, 101, 112, 140, 107, 475, 663, 519], "bin_labels": ["1.00 - 4.40", "4.40 - 7.80", "7.80 - 11.20", "11.20 - 14.60", "14.60 - 18.00", "18.00 - 21.40", "21.40 - 24.80", "24.80 - 28.20", "28.20 - 31.60", "31.60 - 35.00"]}, "stat_summary": {"25%": 18.0, "50%": 28.0, "75%": 31.0, "max": 35.0, "min": 1.0, "std": 9.460236482512686, "mean": 24.190419161676648, "count": 2505.0}, "validity_count": {"valid": 2505, "missing": 0}}, {"key": "ENT_VISIT_DATE", "type": "object", "validity_count": {"valid": 2505, "missing": 0}}, {"key": "WEIGHT", "type": "int64", "histogram": {"counts": [310, 230, 251, 248, 229, 241, 232, 249, 248, 267], "bin_labels": ["38.00 - 47.10", "47.10 - 56.20", "56.20 - 65.30", "65.30 - 74.40", "74.40 - 83.50", "83.50 - 92.60", "92.60 - 101.70", "101.70 - 110.80", "110.80 - 119.90", "119.90 - 129.00"]}, "stat_summary": {"25%": 60.0, "50%": 83.0, "75%": 106.0, "max": 129.0, "min": 38.0, "std": 26.83753650157789, "mean": 82.88423153692615, "count": 2505.0}, "validity_count": {"valid": 2505, "missing": 0}}, {"key": "HEIGHT", "type": "int64", "histogram": {"counts": [274, 248, 224, 229, 209, 273, 263, 249, 236, 300], "bin_labels": ["148.00 - 152.20", "152.20 - 156.40", "156.40 - 160.60", "160.60 - 164.80", "164.80 - 169.00", "169.00 - 173.20", "173.20 - 177.40", "177.40 - 181.60", "181.60 - 185.80", "185.80 - 190.00"]}, "stat_summary": {"25%": 158.0, "50%": 170.0, "75%": 180.0, "max": 190.0, "min": 148.0, "std": 12.41860357357178, "mean": 169.34131736526948, "count": 2505.0}, "validity_count": {"valid": 2505, "missing": 0}}, {"key": "BMI", "type": "float64", "histogram": {"counts": [203, 360, 386, 365, 397, 299, 241, 131, 87, 36], "bin_labels": ["10.50 - 15.26", "15.26 - 20.02", "20.02 - 24.78", "24.78 - 29.54", "29.54 - 34.30", "34.30 - 39.06", "39.06 - 43.82", "43.82 - 48.58", "48.58 - 53.34", "53.34 - 58.10"]}, "stat_summary": {"25%": 20.9, "50%": 28.6, "75%": 36.7, "max": 58.1, "min": 10.5, "std": 10.538669992831505, "mean": 29.362874251497004, "count": 2505.0}, "validity_count": {"valid": 2505, "missing": 0}}, {"key": "ECOG", "type": "int64", "histogram": {"counts": [586, 0, 556, 0, 0, 834, 0, 322, 0, 207], "bin_labels": ["0.00 - 0.40", "0.40 - 0.80", "0.80 - 1.20", "1.20 - 1.60", "1.60 - 2.00", "2.00 - 2.40", "2.40 - 2.80", "2.80 - 3.20", "3.20 - 3.60", "3.60 - 4.00"]}, "stat_summary": {"25%": 1.0, "50%": 2.0, "75%": 2.0, "max": 4.0, "min": 0.0, "std": 1.2085227297964372, "mean": 1.6039920159680638, "count": 2505.0}, "validity_count": {"valid": 2505, "missing": 0}}, {"key": "GASTRIC_TUBE", "type": "bool", "validity_count": {"valid": 2505, "missing": 0}}, {"key": "TOBACCO_DATE", "type": "object", "validity_count": {"valid": 2505, "missing": 0}}, {"key": "NECRO_JAW", "type": "float64", "histogram": {"counts": [1926, 0, 134, 0, 0, 101, 0, 65, 0, 37], "bin_labels": ["0.00 - 0.40", "0.40 - 0.80", "0.80 - 1.20", "1.20 - 1.60", "1.60 - 2.00", "2.00 - 2.40", "2.40 - 2.80", "2.80 - 3.20", "3.20 - 3.60", "3.60 - 4.00"]}, "stat_summary": {"25%": 0.0, "50%": 0.0, "75%": 0.0, "max": 4.0, "min": 0.0, "std": 0.8173813602323577, "mean": 0.30004418912947417, "count": 2263.0}, "validity_count": {"valid": 2263, "missing": 242}}, {"key": "ORAL_MUCOSITIS", "type": "float64", "histogram": {"counts": [386, 0, 0, 361, 0, 0, 692, 0, 0, 962], "bin_labels": ["0.00 - 0.30", "0.30 - 0.60", "0.60 - 0.90", "0.90 - 1.20", "1.20 - 1.50", "1.50 - 1.80", "1.80 - 2.10", "2.10 - 2.40", "2.40 - 2.70", "2.70 - 3.00"]}, "stat_summary": {"25%": 1.0, "50%": 2.0, "75%": 3.0, "max": 3.0, "min": 0.0, "std": 1.0906460861281848, "mean": 1.9287796751353603, "count": 2401.0}, "validity_count": {"valid": 2401, "missing": 104}}, {"key": "DEATH_DATE", "type": "object", "validity_count": {"valid": 998, "missing": 1507}}, {"key": "SMOKING_CIGARETTE_QUANTITY", "type": "float64", "histogram": {"counts": [103, 51, 51, 46, 60, 57, 92, 86, 67, 160], "bin_labels": ["1.00 - 2.10", "2.10 - 3.20", "3.20 - 4.30", "4.30 - 5.40", "5.40 - 6.50", "6.50 - 7.60", "7.60 - 8.70", "8.70 - 9.80", "9.80 - 10.90", "10.90 - 12.00"]}, "stat_summary": {"25%": 4.0, "50%": 8.0, "75%": 10.0, "max": 12.0, "min": 1.0, "std": 3.399837016880107, "mean": 7.1371280724450195, "count": 773.0}, "validity_count": {"valid": 773, "missing": 1732}}, {"key": "DYSPHAGIA", "type": "float64", "histogram": {"counts": [240, 0, 0, 458, 0, 0, 828, 0, 0, 835], "bin_labels": ["0.00 - 0.30", "0.30 - 0.60", "0.60 - 0.90", "0.90 - 1.20", "1.20 - 1.50", "1.50 - 1.80", "1.80 - 2.10", "2.10 - 2.40", "2.40 - 2.70", "2.70 - 3.00"]}, "stat_summary": {"25%": 1.0, "50%": 2.0, "75%": 3.0, "max": 3.0, "min": 0.0, "std": 0.9760927307761688, "mean": 1.9563744176196527, "count": 2361.0}, "validity_count": {"valid": 2361, "missing": 144}}]'
                )],
            session)

    insert_data(
        [StudyAgreements(
                            id=1,
                            study_id=1,
                            use_case="HNC",
                            datasets="1,2",
                            status="approved",
                            purpose="Study agreement one purpose",
                            samples="80",
                            pet="None",
                            pet_config="{}",
                            model="NN",
                            label="HNC",
                            legal="Study agreement one legal",
                            created_by=3),

         OrganizationStudyAgreements(
                            study_agreement_id=1,
                            organization_id=2,
                            organization_type="researcher",
                            status="approved"),
         OrganizationStudyAgreements(
                            study_agreement_id=1,
                            organization_id=3,
                            dataset_id=1,
                            organization_type="data_owner",
                            status="approved"),
         OrganizationStudyAgreements(
                            study_agreement_id=1,
                            organization_id=4,
                            dataset_id=2,
                            organization_type="data_owner",
                            status="approved"),
        ], session)

    for table_name in ["roles", "organizations", "users", "studies", "study_agreements", "datasets"]:
        reset_sequences(table_name, "id", session)
if __name__ == "__main__":
    seed_database()
