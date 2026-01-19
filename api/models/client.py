from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from .base import Base

class Client(Base):
	__tablename__ = "client"

	idClient = Column(Integer, primary_key=True, autoincrement=True)

	nomClient = Column(String(100), nullable=False)
	prenomClient = Column(String(100), nullable=False)
	genre = Column(String(10), nullable=True)  # ex : 'F', 'M', 'NB', etc.
	emailClient = Column(String(255), nullable=False, unique=True)
	telephone = Column(String(30), nullable=True)

	# Relations
	# Un client peut avoir plusieurs adresses
	adresses = relationship(
		"Adresse",
		back_populates="client",
		cascade="all, delete-orphan",
	)

	def __repr__(self) -> str:
		return (
			f"<Client(id={self.idClient}, nom='{self.nomClient}', "
			f"prenom='{self.prenomClient}', email='{self.emailClient}')>"
		)