from sqlalchemy import Column, String, Integer, ForeignKey, Enum, TIMESTAMP, Boolean, func
from sqlalchemy.orm import relationship
from .base import Base


class OrganizationUsers(Base):
    __tablename__ = 'organization_users'

    id = Column(Integer, primary_key=True, autoincrement=True,)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=True,)
    organization_id = Column(Integer, ForeignKey('organizations.id'), nullable=True,)
    created_at = Column(TIMESTAMP, nullable=True, default=func.now())
    updated_at = Column(TIMESTAMP, nullable=True, default=func.now(), onupdate=func.now())
    created_by = Column(Integer, ForeignKey('users.id'), nullable=True,)
    updated_by = Column(Integer, ForeignKey('users.id'), nullable=True,)

    created_by_user = relationship('Users', foreign_keys=[created_by])
    updated_by_user = relationship('Users', foreign_keys=[updated_by])
    organization = relationship('Organizations', back_populates='organization_users', foreign_keys=[organization_id])
    user = relationship('Users', back_populates='organization_users', foreign_keys=[user_id])