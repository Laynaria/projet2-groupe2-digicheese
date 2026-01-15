from sqlalchemy import Column, Integer, String
from .base import Base


class Role(Base):
    __tablename__ = "role"

    idRole = Column(Integer, primary_key=True)
    libelleRole = Column(String(255))
