from .admin_user_seed import seed_admin_user
from .objet_seed import seed_objets
from .rel_cond_seed import seed_rel_cond
from .role_seed import seed_roles
from .utilisateur_seed import seed_utilisateurs
from .conditionnement_seed import seed_conditionnement
from .commande_seed import seed_commande
from .detail_commande_seed import seed_detail_commande
from .commune_seed import seed_communes
from .client_seed import seed_clients
from .adresse_seed import seed_adresses
from .detail_commande_objet_seed import seed_detail_commande_objet

def init_seed():
    seed_roles()
    seed_admin_user()
    seed_utilisateurs()
    seed_conditionnement()
    seed_communes()
    seed_clients()
    seed_adresses()
    seed_commande()
    seed_detail_commande()
    seed_rel_cond()
    seed_objets()
    seed_detail_commande_objet()
