from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from db.models.BaseModelClass import BaseModelClass


class UserType(BaseModelClass):
    __tablename__ = "user_type"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(64), nullable=False)
    description = Column(String(256), nullable=True)
    users = relationship("User", back_populates="type")
