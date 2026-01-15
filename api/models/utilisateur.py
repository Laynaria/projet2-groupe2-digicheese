from sqlalchemy import Column, Integer, String
from .base import Base


class Utilisateur(Base):
    __tablename__ = "utilisateur"

    idUtil = Column(Integer, primary_key=True)
    nomUtil = Column(String(255))
    prenomUtil = Column(String(255))
    motDePasse = Column(String(255))
    emailUtil = Column(String(255))
