from sqlalchemy import Column, String, Integer, ForeignKey, Enum, TIMESTAMP, Boolean, func, Text
from sqlalchemy.orm import relationship
from .base import Base


class StudyAgreements(Base):
    __tablename__ = 'study_agreements'

    id = Column(Integer, primary_key=True, autoincrement=True,)
    purpose = Column(Text, nullable=True,)
    participants = Column(String(255), nullable=True,)
    use_case = Column(Enum('HNC', 'SBRT', 'NSCLC', name='study_agreements_use_case_enum'), nullable=True)
    datasets = Column(String(255), nullable=True,)
    samples = Column(Integer, nullable=True,)
    pet = Column(Enum('None', 'CDC_DP', 'ThHE', name='study_agreements_pet_enum'), nullable=True,)
    pet_config = Column(Text, nullable=False,)
    model = Column(Enum("REG_LOG", "NN", name='study_agreements_model_enum'), nullable=False)
    legal = Column(String(30), nullable=True,)
    label = Column(Enum("HNC", "HNC_NECRO_JAW", "HNC_DYSPHAGIA", "HNC_ORAL_MUCOSITIS", name='study_agreements_label_enum'), nullable=False)
    expiration_date = Column(TIMESTAMP, nullable=True,)
    study_id = Column(Integer, ForeignKey('studies.id'), nullable=True,)
    status = Column(Enum('pending', 'approved', 'disapproved', name='study_agreements_status_enum'),
                             nullable=True, default='pending')
    created_at = Column(TIMESTAMP(timezone=True), nullable=True, default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True), nullable=True, default=func.now(), onupdate=func.now())
    created_by = Column(Integer, ForeignKey('users.id'), nullable=True,)
    updated_by = Column(Integer, ForeignKey('users.id'), nullable=True,)

    created_by_user = relationship('Users', foreign_keys=[created_by])
    updated_by_user = relationship('Users', foreign_keys=[updated_by])
    study_agreement_datasets = relationship('StudyAgreementDatasets', back_populates='study_agreement', foreign_keys='StudyAgreementDatasets.study_agreement_id', lazy='dynamic')
    study_agreement_queries = relationship('StudyAgreementQueries', back_populates='study_agreement', foreign_keys='StudyAgreementQueries.study_agreement_id', lazy='dynamic')
    study_agreement_results = relationship('StudyAgreementResults', back_populates='study_agreement', foreign_keys='StudyAgreementResults.study_agreement_id', lazy='dynamic')
    organization_study_agreements = relationship('OrganizationStudyAgreements', back_populates='study_agreement', foreign_keys='OrganizationStudyAgreements.study_agreement_id', lazy='dynamic')
    study = relationship('Studies', back_populates='study_agreements', foreign_keys=[study_id])
