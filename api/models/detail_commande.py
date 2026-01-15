from sqlalchemy import Column, Integer, String, Date, ForeignKey, Index, Float
from .base import Base

class DetailCommande(Base):
	__tablename__ = "detail_commande"

	idDetailCommande = Column(Integer,primary_key=True)
	quantite = Column(Integer)
	colis = Column(String(20))
	commentaire = Column(String(255))
	commande_id = Column(Integer, ForeignKey('commande.idCommande'))


	# __table_args__ = (Index('commmande_index', "cdeComt", "codcli"),)