from sqlalchemy import Column, Integer, String, Date, ForeignKey, Index, Float
from sqlalchemy.orm import relationship
from .base import Base
from .detail_commande_objet import DetailCommandeObjet

class DetailCommande(Base):
	__tablename__ = "detail_commande"

	idDetailCommande = Column(Integer,primary_key=True)
	quantite = Column(Integer)
	colis = Column(String(20))
	commentaire = Column(String(255))
	commande_id = Column(Integer, ForeignKey('commande.idCommande'))

	detailCommandeObjetRelationship = relationship('DetailCommandeObjet', backref='detail_commande_objet', cascade='all, delete')


	# __table_args__ = (Index('commmande_index', "cdeComt", "codcli"),)