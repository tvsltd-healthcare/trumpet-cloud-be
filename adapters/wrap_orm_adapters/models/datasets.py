from sqlalchemy import Column, String, Integer, ForeignKey, TIMESTAMP, func
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
    statistics = Column(Text, nullable=False, )

    created_at = Column(TIMESTAMP, nullable=True, default=func.now())
    updated_at = Column(TIMESTAMP, nullable=True, default=func.now(), onupdate=func.now())
    created_by = Column(Integer, ForeignKey('users.id'), nullable=True, )
    updated_by = Column(Integer, ForeignKey('users.id'), nullable=True, )

    created_by_user = relationship('Users', foreign_keys=[created_by])
    updated_by_user = relationship('Users', foreign_keys=[updated_by])

    organization = relationship('Organizations', foreign_keys=[organization_id])
    study_agreement_datasets = relationship('StudyAgreementDatasets', back_populates='dataset',
                                            foreign_keys='StudyAgreementDatasets.dataset_id', lazy='dynamic')
