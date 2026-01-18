from sqlalchemy import Column, Integer, String, Date, ForeignKey, Index, Float, Boolean
from sqlalchemy.orm import relationship
from .base import Base
from .detail_commande import DetailCommande

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
	client_id = Column(Integer,ForeignKey('client.idClient'))
	conditionnement_id = Column(Integer,ForeignKey('conditionnement.idConditionnement'))

	detailCommandeRelationship = relationship('DetailCommande', backref='detail_commande', cascade='all, delete')

	# __table_args__ = (Index('commmande_index', "cdeComt", "codcli"),)