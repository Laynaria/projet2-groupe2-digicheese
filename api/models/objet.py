from sqlalchemy import Column, Integer, String, Numeric
from .base import Base


class Objet(Base):
	__tablename__ = "objet"

	idObjet = Column(Integer,primary_key=True)
	libelle = Column(String(50), default=None)
	taille = Column(String(50), default=None)
	poids = Column(Numeric, default=0.0000)
	bIndispo = Column(Integer, default=0)
	points = Column(Integer, default=0)
