from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship

from db.models.BaseModelClass import BaseModelClass


class UserType(BaseModelClass):
    __tablename__ = "user_type"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(64), nullable=False)
    description = Column(String(256), nullable=True)
    is_admin = Column(Boolean, nullable=False)
    users = relationship("User", back_populates="type")
