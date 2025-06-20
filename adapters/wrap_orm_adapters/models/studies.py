from sqlalchemy import Column, String, Integer, ForeignKey, Enum, TIMESTAMP, Boolean, func
from sqlalchemy.orm import relationship
from .base import Base
from sqlalchemy.types import Text


class Studies(Base):
    __tablename__ = 'studies'

    id = Column(Integer, primary_key=True, autoincrement=True,)
    name = Column(String(25), nullable=True,)
    description = Column(Text, nullable=False,)
    status = Column(Enum('active', 'paused', 'completed', name='studies_status_enum'), nullable=True, default='active')
    result = Column(Text, nullable=True,)
    purpose = Column(Text, nullable=True,)
    organization_id = Column(Integer, nullable=False)
    created_at = Column(TIMESTAMP, nullable=True, default=func.now())
    updated_at = Column(TIMESTAMP, nullable=True, default=func.now(), onupdate=func.now())
    created_by = Column(Integer, ForeignKey('users.id'), nullable=True,)
    updated_by = Column(Integer, ForeignKey('users.id'), nullable=True,)

    created_by_user = relationship('Users', foreign_keys=[created_by])
    updated_by_user = relationship('Users', foreign_keys=[updated_by])
    study_collaborators = relationship('StudyUsers', back_populates='study', foreign_keys='StudyUsers.study_id', lazy='dynamic')
    study_agreements = relationship('StudyAgreements', back_populates='study', foreign_keys='StudyAgreements.study_id', lazy='dynamic')