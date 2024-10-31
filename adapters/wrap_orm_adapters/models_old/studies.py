from sqlalchemy import Column, String, Integer, ForeignKey, Enum, TIMESTAMP, Boolean, func
from sqlalchemy.orm import relationship
# from sqlalchemy.orm import declarative_base
from sqlalchemy.types import Text
from sqlalchemy.types import Text
from sqlalchemy.types import Text
# from .users import Users
# from .study_users import StudyUsers
# from .study_agreements import StudyAgreements


# Base = declarative_base()
from base import Base


class Studies(Base):
    __tablename__ = 'studies'

    id = Column(Integer, primary_key=True, nullable=True, unique=True, autoincrement=True,)
    name = Column(String(25), nullable=True,)
    description = Column(Text, nullable=False,)
    status = Column(Enum('active', 'paused', 'completed', name='status_enum'), nullable=True, default='active')
    result = Column(Text, nullable=True,)
    purpose = Column(Text, nullable=True,)
    created_at = Column(TIMESTAMP, nullable=True, default=func.now())
    updated_at = Column(TIMESTAMP, nullable=False, default=func.now(), onupdate=func.now())
    created_by = Column(Integer, ForeignKey('users.id'), nullable=True,)
    updated_by = Column(Integer, ForeignKey('users.id'), nullable=False,)

    created_by_user = relationship('Users', foreign_keys=[created_by])
    updated_by_user = relationship('Users', foreign_keys=[updated_by])
    study_collaborators = relationship('StudyUsers', back_populates='study', foreign_keys='StudyUsers.study_id', lazy='dynamic')
    study_agreements = relationship('StudyAgreements', back_populates='study', foreign_keys='StudyAgreements.study_id', lazy='dynamic')