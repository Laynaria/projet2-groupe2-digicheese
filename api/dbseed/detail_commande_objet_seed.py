import os
import random
from sqlalchemy.orm import Session

from ..database import SessionLocal
from ..models import DetailCommandeObjet, DetailCommande, Objet

def seed_detail_commande_objet():
    if os.getenv("SEED_DB", "false").lower() != "true":
        print("SEED_DB désactivé - seed ignoré")
        return
    
    nb = int(os.getenv("SEED_NB_DETAIL_COMMANDE_OBJET", "40"))
    db: Session = SessionLocal()

    try:
        count = db.query(DetailCommandeObjet).count()
        if count > 0:
            print("Table detail_commande_objet déjà seedée")
            return
        
        detailCommandes: list[DetailCommande] = db.query(DetailCommande)
        countDetailCommandes: int = db.query(DetailCommande).count()
        objets: list[Objet] = db.query(Objet)
        countObjets: int = db.query(Objet).count()


        detail_commandes = []
        for _ in range(nb):
            new_detail_commande = DetailCommandeObjet(
                detailleCommande_id=detailCommandes[random.randint(1, countDetailCommandes - 1)].idDetailCommande,
                objet_id=objets[random.randint(1, countObjets - 1)].idObjet
            )
            detail_commandes.append(new_detail_commande)

        db.add_all(detail_commandes)
        db.commit()
        print(f"Seed terminé")

    except Exception as e:
        db.rollback()
        raise
    finally:
        db.close()