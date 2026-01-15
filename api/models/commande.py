from sqlalchemy import Column, Integer, String, Date, ForeignKey, Index, Float, Boolean
from .base import Base

class Commande(Base):
	__tablename__ = "commande"

	idCommande = Column(Integer,primary_key=True)
	date = Column(Date)
	timbreClient = Column(Float)
	timbreCode = Column(Float)
	chequeClient = Column(Float)
	commentaireCommande = Column(String(255), default=None)
	nbColis = Column(Integer)
	bArchive = Column(Boolean)
	conditionnement_id = Column(Integer,ForeignKey('conditionnement.idConditionnement'))

	# __table_args__ = (Index('commmande_index', "cdeComt", "codcli"),)