from sqlalchemy import Column, String, Integer, ForeignKey, Enum, TIMESTAMP, Boolean, func
from sqlalchemy.orm import relationship
from .base import Base
from sqlalchemy.dialects.mysql import LONGBLOB


class Files(Base):
    __tablename__ = 'files'

    id = Column(Integer, primary_key=True, nullable=True, unique=True, autoincrement=True,)
    type = Column(Enum('custom', 'legal', 'personal', 'other', name='type_enum'), nullable=True, default='custom')
    buffer = Column(LONGBLOB, nullable=True,)
    created_at = Column(TIMESTAMP, nullable=True, default=func.now())
    updated_at = Column(TIMESTAMP, nullable=False, default=func.now(), onupdate=func.now())
    created_by = Column(Integer, ForeignKey('users.id'), nullable=True,)
    updated_by = Column(Integer, ForeignKey('users.id'), nullable=False,)

    created_by_user = relationship('Users', foreign_keys=[created_by])
    updated_by_user = relationship('Users', foreign_keys=[updated_by])