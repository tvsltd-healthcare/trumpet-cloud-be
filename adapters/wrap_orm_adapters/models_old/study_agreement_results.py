from sqlalchemy import Column, String, Integer, ForeignKey, Enum, TIMESTAMP, Boolean, func
from sqlalchemy.orm import relationship
# from sqlalchemy.orm import declarative_base
from sqlalchemy.types import Text
# from .users import Users
# from .study_agreements import StudyAgreements


from base import Base


class StudyAgreementResults(Base):
    __tablename__ = 'study_agreement_results'

    id = Column(Integer, primary_key=True, nullable=True, unique=True, autoincrement=True,)
    study_agreement_id = Column(Integer, ForeignKey('study_agreements.id'), nullable=True,)
    specification = Column(Text, nullable=True,)
    version = Column(String(20), nullable=True,)
    status = Column(Enum('approved', 'disapproved', 'blocked', 'pending_registration', name='status_enum'), nullable=True, default='approved')
    created_at = Column(TIMESTAMP, nullable=True, default=func.now())
    updated_at = Column(TIMESTAMP, nullable=False, default=func.now(), onupdate=func.now())
    created_by = Column(Integer, ForeignKey('users.id'), nullable=True,)
    updated_by = Column(Integer, ForeignKey('users.id'), nullable=False,)

    created_by_user = relationship('Users', foreign_keys=[created_by])
    updated_by_user = relationship('Users', foreign_keys=[updated_by])
    study_agreement = relationship('StudyAgreements', back_populates='study_agreement_results', foreign_keys=[study_agreement_id])