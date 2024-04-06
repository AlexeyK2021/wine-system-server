from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from db.models.BaseModelClass import BaseModelClass
from db.models.UserType import UserType


class User(BaseModelClass):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(128), nullable=False)
    login = Column(String(64), nullable=False)
    password = Column(String(64), nullable=False)

    type_id = Column(Integer, ForeignKey("user_type.id"))
    type = relationship("UserType", back_populates="users")
    # type = relationship("UserType", back_populates="users")
    user_logs = relationship("UserLog", back_populates="user")
