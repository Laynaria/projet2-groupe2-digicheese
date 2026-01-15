from sqlalchemy import Column, Integer, String, Date, ForeignKey, Index, Float
from .base import Base

class DetailCommandeObjet(Base):
	__tablename__ = "detail_commande_objet"

	idDetailCommandeObjet = Column(Integer,primary_key=True)
	detailleCommande_id = Column(Integer,ForeignKey('detail_commande.idDetailCommande'))
	objet_id = Column(Integer,ForeignKey('objet.idDetailCommande'))


	# __table_args__ = (Index('commmande_index', "cdeComt", "codcli"),)