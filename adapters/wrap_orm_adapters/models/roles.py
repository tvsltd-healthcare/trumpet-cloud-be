from sqlalchemy import Column, String, Integer, ForeignKey, Enum, TIMESTAMP, Boolean, func
from sqlalchemy.orm import relationship
from .base import Base
from .user_roles import UserRoles


class Roles(Base):
    __tablename__ = 'roles'

    id = Column(Integer, primary_key=True, nullable=True, unique=True, autoincrement=True,)
    name = Column(String(30), nullable=True, unique=True,)
    created_at = Column(TIMESTAMP, nullable=True, default=func.now())
    updated_at = Column(TIMESTAMP, nullable=False, default=func.now(), onupdate=func.now())
    created_by = Column(Integer, ForeignKey('users.id'), nullable=True,)
    updated_by = Column(Integer, ForeignKey('users.id'), nullable=True,)

    created_by_user = relationship('Users', foreign_keys=[created_by])
    updated_by_user = relationship('Users', foreign_keys=[updated_by])
    user_role = relationship('UserRoles', back_populates='role', foreign_keys='UserRoles.role_id', lazy='dynamic')