from sqlalchemy import Column, String, Integer, ForeignKey, Enum, TIMESTAMP, Boolean, func
from sqlalchemy.orm import relationship
from .base import Base


class StudyUsers(Base):
    __tablename__ = 'study_users'

    id = Column(Integer, primary_key=True, nullable=True, unique=True, autoincrement=True,)
    study_id = Column(Integer, ForeignKey('studies.id'), nullable=True,)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=True,)
    created_at = Column(TIMESTAMP, nullable=True, default=func.now())
    updated_at = Column(TIMESTAMP, nullable=False, default=func.now(), onupdate=func.now())
    created_by = Column(Integer, ForeignKey('users.id'), nullable=True,)
    updated_by = Column(Integer, ForeignKey('users.id'), nullable=True,)

    created_by_user = relationship('Users', foreign_keys=[created_by])
    updated_by_user = relationship('Users', foreign_keys=[updated_by])
    study = relationship('Studies', back_populates='study_collaborators', foreign_keys=[study_id])
    user = relationship('Users', back_populates='study_collaborators', foreign_keys=[user_id])