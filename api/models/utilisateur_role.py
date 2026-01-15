from sqlalchemy import Column, Integer, ForeignKey
from .base import Base


class UtilisateurRole(Base):
    __tablename__ = "utilisateur_role"

    idUtil = Column(Integer, ForeignKey("utilisateur.idUtil"), primary_key=True)
    idRole = Column(Integer, ForeignKey("role.idRole"), primary_key=True)
