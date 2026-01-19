from pydantic import BaseModel
from typing import Optional

class ConditionnementBase(BaseModel):
	"""Base schema for conditionnement data."""
	libelle: str
	poidsConditionnement: float
	ordreImpression: int
	
class ConditionnementPost(ConditionnementBase):
	"""Schema for creating new conditionnement."""
	pass

class ConditionnementPatch(ConditionnementBase):
	"""Schema for updating an existing conditionnement.
	Values are all optionnal to update only what you want.
	"""
	libelle: Optional[str] = None
	poidsConditionnement: Optional[float] = None
	ordreImpression: Optional[int] = None

class ConditionnementInDB(ConditionnementBase):
	"""Schema for conditionnement data stored in Database"""
	idConditionnement: int

	class Config:
		from_attributes = True