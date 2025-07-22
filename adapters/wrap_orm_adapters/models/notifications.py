from sqlalchemy import Column, String, Integer, ForeignKey, Enum, TIMESTAMP, Boolean, func, Text
from sqlalchemy.orm import relationship
from .base import Base


class Notifications(Base):
    __tablename__ = 'notifications'
    id = Column(Integer, primary_key=True, autoincrement=True,)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=True, )
    message = Column(Text, nullable=True, )
    is_read = Column(Boolean, nullable=False, default=False)
    type = Column(Enum('organization_approved', 'user_approved', name='notifications_type_enum'), nullable=True, )
    read_at = Column(TIMESTAMP, nullable=True, default=func.now())
    created_at = Column(TIMESTAMP, nullable=True, default=func.now())
    updated_at = Column(TIMESTAMP, nullable=True, default=func.now(), onupdate=func.now())
    created_by = Column(Integer, ForeignKey('users.id'), nullable=True, )
    updated_by = Column(Integer, ForeignKey('users.id'), nullable=True, )

    created_by_user = relationship('Users', foreign_keys=[created_by])
    updated_by_user = relationship('Users', foreign_keys=[updated_by])
    user = relationship('Users', back_populates='notifications', foreign_keys=[user_id])
