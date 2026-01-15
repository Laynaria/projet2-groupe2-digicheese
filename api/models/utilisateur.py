from sqlalchemy import Column, Integer, String
from .base import Base


class Utilisateur(Base):
    __tablename__ = "utilisateur"

    idUtil = Column(Integer, primary_key=True, index=True)
    nomUtil = Column(String(255), nullable=False)
    prenomUtil = Column(String(255), nullable=False)
    motDePasse = Column(String(255), nullable=False)
    emailUtil = Column(String(255), unique=True, nullable=False)
