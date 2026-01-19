from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from .base import Base


class Role(Base):
    __tablename__ = "role"

    idRole = Column(Integer, primary_key=True)
    libelleRole = Column(String(255), unique=True, nullable=False)

    utilisateurs = relationship(
        "Utilisateur",
        secondary="utilisateur_role",
        back_populates="roles",
    )