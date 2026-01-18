from .admin_user_seed import seed_admin_user
from .objet_seed import seed_objets
from .role_seed import seed_roles
from .utilisateur_seed import seed_utilisateurs
from .commune_seed import seed_communes
from .client_seed import seed_clients
from .adresse_seed import seed_adresses

def init_seed():
    seed_roles()
    seed_admin_user()
    seed_utilisateurs()
    seed_communes()
    seed_clients()
    seed_adresses()
    seed_objets()