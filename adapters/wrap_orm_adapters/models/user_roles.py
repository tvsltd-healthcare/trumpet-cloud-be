from sqlalchemy import Column, String, Integer, ForeignKey, Enum, TIMESTAMP, Boolean, func
from sqlalchemy.orm import relationship
from base import Base


class UserRoles(Base):
    __tablename__ = 'user_roles'

    id = Column(Integer, primary_key=True, nullable=True, unique=True, autoincrement=True,)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=True,)
    role_id = Column(Integer, ForeignKey('roles.id'), nullable=True,)
    created_at = Column(TIMESTAMP, nullable=True, default=func.now())
    updated_at = Column(TIMESTAMP, nullable=False, default=func.now(), onupdate=func.now())
    created_by = Column(Integer, ForeignKey('users.id'), nullable=True,)
    updated_by = Column(Integer, ForeignKey('users.id'), nullable=False,)

    created_by_user = relationship('Users', foreign_keys=[created_by])
    updated_by_user = relationship('Users', foreign_keys=[updated_by])
    user = relationship('Users', back_populates='user_role', foreign_keys=[user_id])
    role = relationship('Roles', back_populates='user_role', foreign_keys=[role_id])