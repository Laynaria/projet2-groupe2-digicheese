#!/bin/sh
set -e

echo "Running DB seed"
python -c "from api.dbseed.role_seed import seed_roles; seed_roles()"
python -c "from api.dbseed.admin_user_seed import seed_admin_user; seed_admin_user()"
python -c "from api.dbseed.utilisateur_seed import seed_utilisateurs; seed_utilisateurs()"
python -c "from api.dbseed.objet_seed import seed_objets; seed_objets()"

echo "Starting API"
exec uvicorn api.main:app --host 0.0.0.0 --port 80
