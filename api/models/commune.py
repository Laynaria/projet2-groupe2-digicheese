from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from .base import Base

class Commune(Base):
    __tablename__ = "commune"

    idCommune = Column(Integer, primary_key=True, autoincrement=True)
    cp = Column(String(10), nullable=False)
    nom_commune = Column(String(100), nullable=False)
    departement = Column(String(100), nullable=True)

    # Relations
    # Une commune possède plusieurs adresses
    adresses = relationship(
        "Adresse",
        back_populates="commune",
        cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:
        return f"<Commune(id={self.idCommune}, cp={self.cp}, nom={self.nom_commune})>"
