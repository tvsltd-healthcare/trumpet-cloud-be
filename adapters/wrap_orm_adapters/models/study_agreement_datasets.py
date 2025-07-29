from sqlalchemy import Column, String, Integer, ForeignKey, Enum, TIMESTAMP, Boolean, func
from sqlalchemy.orm import relationship
from .base import Base
from sqlalchemy.types import Text


class StudyAgreementDatasets(Base):
    __tablename__ = 'study_agreement_datasets'

    id = Column(Integer, primary_key=True, autoincrement=True,)
    description = Column(Text, nullable=True,)
    study_agreement_id = Column(Integer, ForeignKey('study_agreements.id'), nullable=True,)
    dataset_id = Column(Integer, ForeignKey('datasets.id'), nullable=True,)
    created_at = Column(TIMESTAMP(timezone=True), nullable=True, default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True), nullable=True, default=func.now(), onupdate=func.now())
    created_by = Column(Integer, ForeignKey('users.id'), nullable=True,)
    updated_by = Column(Integer, ForeignKey('users.id'), nullable=True,)

    created_by_user = relationship('Users', foreign_keys=[created_by])
    updated_by_user = relationship('Users', foreign_keys=[updated_by])
    study_agreement = relationship('StudyAgreements', back_populates='study_agreement_datasets', foreign_keys=[study_agreement_id])
    dataset = relationship('Datasets', back_populates='study_agreement_datasets', foreign_keys=[dataset_id])
