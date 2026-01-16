from pydantic import BaseModel
from typing import Optional

class DetailCommandeBase(BaseModel):
	"""Base schema for detail_commande data."""
	quantite: int
	colis: str
	commentaire: str
	commande_id: int
	
class DetailCommandePost(DetailCommandeBase):
	"""Schema for creating new detail_commande."""
	pass

class DetailCommandePatch(DetailCommandeBase):
	"""Schema for updating an existing detail_commande.
	Values are all optionnal to update only what you want.
	"""
	quantite: Optional[int] = None
	colis: Optional[str] = None
	commentaire: Optional[str] = None
	commande_id: Optional[int] = None

class DetailCommandeInDB(DetailCommandeBase):
	"""Schema for detail_commande data stored in Database"""
	idDetailCommande: int

	class Config:
		from_attributes = True