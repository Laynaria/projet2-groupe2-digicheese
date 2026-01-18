from .admin_user_seed import seed_admin_user
from .objet_seed import seed_objets
from .role_seed import seed_roles
from .utilisateur_seed import seed_utilisateurs
from .conditionnement_seed import seed_conditionnement
from .commande_seed import seed_commande

def init_seed():
    seed_roles()
    seed_admin_user()
    seed_utilisateurs()
    seed_objets()
    seed_conditionnement()
    seed_commande()