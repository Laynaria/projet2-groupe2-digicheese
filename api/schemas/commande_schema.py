from pydantic import BaseModel
from datetime import date
from typing import Optional

class CommandeBase(BaseModel):
	"""Base schema for commande data."""
	date: date
	timbreClient: float
	timbreCode: float
	chequeClient: float
	commentaireCommande: Optional[str] = None
	nbColis: int
	bArchive : bool
	client_id: int
	conditionnement_id: int
	
class CommandePost(CommandeBase):
	"""Schema for creating new commande."""
	pass

class CommandePatch(CommandeBase):
	"""Schema for updating an existing commande.
	Values are all optionnal to update only what you want.
	"""
	timbreClient: Optional[float] = None
	timbreCode: Optional[float] = None
	chequeClient: Optional[float] = None
	nbColis: Optional[int] = None
	bArchive : Optional[bool] = None
	client_id: Optional[int] = None
	conditionnement_id: Optional[int] = None

class CommandeInDB(CommandeBase):
	"""Schema for commande data stored in Database"""
	idCommande: int

	class Config:
		from_attributes = True