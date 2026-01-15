from sqlalchemy import Column, Integer
from .base import Base


class RelCond(Base):
    __tablename__ = "rel_cond"

    idRelCond = Column(Integer, primary_key=True)
    quantiteObjet = Column(Integer)
