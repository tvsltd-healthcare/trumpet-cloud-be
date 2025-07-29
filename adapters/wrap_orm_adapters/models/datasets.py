from sqlalchemy import Column, String, Integer, ForeignKey, TIMESTAMP, func, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.types import Text

from .base import Base


class Datasets(Base):
    __tablename__ = 'datasets'

    id = Column(Integer, primary_key=True, autoincrement=True, )
    don_uid = Column(String(50), nullable=False, )
    organization_id = Column(Integer, ForeignKey('organizations.id'), nullable=True, )

    title = Column(String(100), nullable=False, )
    about = Column(Text, nullable=False, )
    use_case = Column(Enum('HNC', 'SBRT', 'NSCLC', name='datasets_use_case_enum'), nullable=False)
    statistics = Column(Text, nullable=False, )

    temporal_coverage_start = Column(TIMESTAMP, nullable=True)
    temporal_coverage_end = Column(TIMESTAMP, nullable=True)
    geospatial_coverage = Column(Text, nullable=True, )
    doi_citation = Column(Text, nullable=True, )
    provenance = Column(Text, nullable=True, )
    license_title = Column(String(255), nullable=True, )
    license_details =  Column(Text, nullable=True, )

    created_at = Column(TIMESTAMP, nullable=True, default=func.now())
    updated_at = Column(TIMESTAMP, nullable=True, default=func.now(), onupdate=func.now())
    created_by = Column(Integer, ForeignKey('users.id'), nullable=True, )
    updated_by = Column(Integer, ForeignKey('users.id'), nullable=True, )

    created_by_user = relationship('Users', foreign_keys=[created_by])
    updated_by_user = relationship('Users', foreign_keys=[updated_by])

    organization = relationship('Organizations', foreign_keys=[organization_id])
    study_agreement_datasets = relationship('StudyAgreementDatasets', back_populates='dataset',
                                            foreign_keys='StudyAgreementDatasets.dataset_id', lazy='dynamic')
    organization_study_agreements = relationship('OrganizationStudyAgreements', back_populates='dataset', foreign_keys='OrganizationStudyAgreements.dataset_id', lazy='dynamic')
