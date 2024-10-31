from sqlalchemy import Column, String, Integer, ForeignKey, Enum, TIMESTAMP, Boolean, func
from sqlalchemy.orm import relationship
# from sqlalchemy.orm import declarative_base
# from .users import Users
# from .study_agreement_datasets import StudyAgreementDatasets
# from .study_agreement_queries import StudyAgreementQueries
# from .study_agreement_results import StudyAgreementResults
# from .studies import Studies


from base import Base


class StudyAgreements(Base):
    __tablename__ = 'study_agreements'

    id = Column(Integer, primary_key=True, nullable=True, unique=True, autoincrement=True,)
    purpose = Column(String(30), nullable=True, unique=True,)
    legal = Column(String(30), nullable=True, unique=True,)
    study_privacy_budget = Column(Integer, nullable=True, unique=True,)
    expiration_date = Column(TIMESTAMP, nullable=True,)
    study_id = Column(Integer, ForeignKey('studies.id'), nullable=True,)
    created_at = Column(TIMESTAMP, nullable=True, default=func.now())
    updated_at = Column(TIMESTAMP, nullable=False, default=func.now(), onupdate=func.now())
    created_by = Column(Integer, ForeignKey('users.id'), nullable=True,)
    updated_by = Column(Integer, ForeignKey('users.id'), nullable=False,)

    created_by_user = relationship('Users', foreign_keys=[created_by])
    updated_by_user = relationship('Users', foreign_keys=[updated_by])
    study_agreement_datasets = relationship('StudyAgreementDatasets', back_populates='study_agreement', foreign_keys='StudyAgreementDatasets.study_agreement_id', lazy='dynamic')
    study_agreement_queries = relationship('StudyAgreementQueries', back_populates='study_agreement', foreign_keys='StudyAgreementQueries.study_agreement_id', lazy='dynamic')
    study_agreement_results = relationship('StudyAgreementResults', back_populates='study_agreement', foreign_keys='StudyAgreementResults.study_agreement_id', lazy='dynamic')
    study = relationship('Studies', back_populates='study_agreements', foreign_keys=[study_id])