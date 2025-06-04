from sqlalchemy import Column, String, Integer, ForeignKey, Enum, TIMESTAMP, Boolean, func
from sqlalchemy.orm import relationship
from .base import Base


class Organizations(Base):
    __tablename__ = 'organizations'

    id = Column(Integer, primary_key=True, autoincrement=True,)
    name = Column(String(30), nullable=True, unique=True,)
    email = Column(String(40), nullable=True, unique=True,)
    address = Column(String(50), nullable=False,)
    phone = Column(String(20), nullable=False, unique=True,)
    host = Column(String(100), nullable=True, unique=True, )
    status = Column(Enum('approved', 'disapproved', 'blocked', 'pending', name='organizations_status_enum'), nullable=True, default='pending')
    type = Column(Enum('governance', 'data_owner', 'researcher', name='organizations_type_enum'), nullable=True,)
    created_at = Column(TIMESTAMP, nullable=True, default=func.now())
    updated_at = Column(TIMESTAMP, nullable=False, default=func.now(), onupdate=func.now())
    created_by = Column(Integer, ForeignKey('users.id'), nullable=True,)
    updated_by = Column(Integer, ForeignKey('users.id'), nullable=True,)

    created_by_user = relationship('Users', foreign_keys=[created_by])
    updated_by_user = relationship('Users', foreign_keys=[updated_by])
    organization_users = relationship('OrganizationUsers', back_populates='organization', foreign_keys='OrganizationUsers.organization_id', lazy='dynamic')
    organization_study_agreements = relationship('OrganizationStudyAgreements', back_populates='organization', foreign_keys='OrganizationStudyAgreements.organization_id', lazy='dynamic')
