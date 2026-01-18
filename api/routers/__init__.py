from api.routers.dependencies import get_current_utilisateur

from fastapi import APIRouter, Depends
from .auth_router import router as auth_router
from .utilisateur_router import router as utilisateur_router
from .client_router import router as router_client
from .objet_router import router as router_objet
from .commande_router import router as router_commande
from .conditionnement_router import router as router_conditionnement
from .detail_commande_router import router as router_detail_commande
from .detail_commande_objet_router import router as router_detail_commande_objet
from .role_router import router as role_router
from .commune_router import router as commune_router
from .adresse_router import router as adresse_router
from .rel_cond_router import router as rel_cond_router

router = APIRouter(prefix="/api/v1")
router.include_router(auth_router)

protected_router = APIRouter(
    dependencies=[Depends(get_current_utilisateur)]
)
protected_router.include_router(router_client)
protected_router.include_router(rel_cond_router)
protected_router.include_router(router_objet)
protected_router.include_router(router_commande)
protected_router.include_router(router_conditionnement)
protected_router.include_router(router_detail_commande)
protected_router.include_router(router_detail_commande_objet)
protected_router.include_router(auth_router)
protected_router.include_router(utilisateur_router)
protected_router.include_router(role_router)
protected_router.include_router(commune_router)
protected_router.include_router(adresse_router)

router.include_router(protected_router)