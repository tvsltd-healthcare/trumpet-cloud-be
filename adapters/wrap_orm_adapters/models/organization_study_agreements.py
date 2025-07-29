from sqlalchemy import Column, Integer, ForeignKey, Enum, TIMESTAMP, func
from sqlalchemy.orm import relationship

from .base import Base


class OrganizationStudyAgreements(Base):
    __tablename__ = 'organization_study_agreements'
    id = Column(Integer, primary_key=True, autoincrement=True, )
    organization_id = Column(Integer, ForeignKey('organizations.id'), nullable=True, )
    study_agreement_id = Column(Integer, ForeignKey('study_agreements.id'), nullable=True, )
    dataset_id = Column(Integer, ForeignKey('datasets.id'), nullable=True, )
    organization_type = Column(Enum('researcher', 'data_owner', name='organization_study_agreements_organization_type_enum'),
                             nullable=True, default='data_owner')

    status = Column(Enum('pending', 'approved', 'disapproved', name='study_agreements_status_enum'),
                             nullable=True, default='pending')

    created_at = Column(TIMESTAMP, nullable=True, default=func.now())
    updated_at = Column(TIMESTAMP, nullable=True, default=func.now(), onupdate=func.now())
    created_by = Column(Integer, ForeignKey('users.id'), nullable=True, )
    updated_by = Column(Integer, ForeignKey('users.id'), nullable=True, )

    created_by_user = relationship('Users', foreign_keys=[created_by])
    updated_by_user = relationship('Users', foreign_keys=[updated_by])

    study_agreement = relationship('StudyAgreements', back_populates='organization_study_agreements',
                                   foreign_keys=[study_agreement_id])
    organization = relationship('Organizations', back_populates='organization_study_agreements',
                                foreign_keys=[organization_id])
    dataset = relationship('Datasets', back_populates='organization_study_agreements',
                                foreign_keys=[dataset_id])
