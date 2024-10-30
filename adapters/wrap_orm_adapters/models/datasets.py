from sqlalchemy import Column, String, Integer, ForeignKey, Enum, TIMESTAMP, Boolean, func
from sqlalchemy.orm import relationship
from .base import Base
from sqlalchemy.types import Text
from .study_agreement_datasets import StudyAgreementDatasets


class Datasets(Base):
    __tablename__ = 'datasets'

    id = Column(Integer, primary_key=True, nullable=True, unique=True, autoincrement=True,)
    name = Column(String(25), nullable=True,)
    meta_data = Column(Text, nullable=True,)
    statistics = Column(Text, nullable=False,)
    path = Column(Text, nullable=False,)
    privacy_level = Column(Enum('public', 'confidential', 'highly_confidential', name='privacy_level_enum'), nullable=True, default='confidential')
    created_at = Column(TIMESTAMP, nullable=True, default=func.now())
    updated_at = Column(TIMESTAMP, nullable=False, default=func.now(), onupdate=func.now())
    created_by = Column(Integer, ForeignKey('users.id'), nullable=True,)
    updated_by = Column(Integer, ForeignKey('users.id'), nullable=True,)

    created_by_user = relationship('Users', foreign_keys=[created_by])
    updated_by_user = relationship('Users', foreign_keys=[updated_by])
    study_agreement_datasets = relationship('StudyAgreementDatasets', back_populates='dataset', foreign_keys='StudyAgreementDatasets.dataset_id', lazy='dynamic')