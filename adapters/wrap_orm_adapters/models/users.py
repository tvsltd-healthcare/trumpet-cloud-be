from sqlalchemy import Column, String, Integer, ForeignKey, Enum, TIMESTAMP, Boolean, func
from sqlalchemy.orm import relationship
from .base import Base


class Users(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True,)
    first_name = Column(String(30), nullable=True,)
    last_name = Column(String(30), nullable=True,)
    email = Column(String(40), nullable=True, unique=True,)
    password = Column(String(255), nullable=True,)
    status = Column(Enum('approved', 'disapproved', 'blocked', 'pending', 'deleted', name='users_status_enum'), nullable=True, default='pending')
    phone = Column(String(20), nullable=True, unique=True,)
    created_at = Column(TIMESTAMP(timezone=True), nullable=True, default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True), nullable=True, default=func.now(), onupdate=func.now())
    created_by = Column(Integer, ForeignKey('users.id'), nullable=True,)
    updated_by = Column(Integer, ForeignKey('users.id'), nullable=True,)

    created_by_user = relationship('Users', foreign_keys=[created_by])
    updated_by_user = relationship('Users', foreign_keys=[updated_by])
    organization_users = relationship('OrganizationUsers', back_populates='user', foreign_keys='OrganizationUsers.user_id')
    user_role = relationship('UserRoles', back_populates='user', foreign_keys='UserRoles.user_id')
    study_collaborators = relationship('StudyUsers', back_populates='user', foreign_keys='StudyUsers.user_id', lazy='dynamic')
    notifications = relationship('Notifications', back_populates='user', foreign_keys='Notifications.user_id', lazy='dynamic')
