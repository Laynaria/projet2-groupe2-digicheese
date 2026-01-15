from sqlalchemy import Column, Integer, String, Float
from .base import Base

class Conditionnement(Base):
	__tablename__ = "conditionnement"

	idConditionnement = Column(Integer,primary_key=True)
	libelle = Column(String(50))
	poidsConditionnement = Column(Float)
	ordreImpression = Column(Integer)