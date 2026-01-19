from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from .base import Base

class Adresse(Base):
    __tablename__ = "adresse"

    idAdresse = Column(Integer, primary_key=True, autoincrement=True)

    compAdresse1 = Column(String(255), nullable=True)
    compAdresse2 = Column(String(255), nullable=True)
    compAdresse3 = Column(String(255), nullable=True)

    numeroVoie = Column(String(10), nullable=False)
    nomVoie = Column(String(255), nullable=False)

    # FK vers commune
    idCommune = Column(Integer, ForeignKey("commune.idCommune"), nullable=False)

    # FK vers client
    idClient = Column(Integer, ForeignKey("client.idClient"), nullable=False)

    # Relations
    commune = relationship("Commune", back_populates="adresses")
    client = relationship("Client", back_populates="adresses")

    def __repr__(self) -> str:
        return (
            f"<Adresse(id={self.idAdresse}, voie='{self.numeroVoie} {self.nomVoie}', "
            f"cp_commune={self.commune.cp if self.commune else None})>"
        )
