from fastapi import APIRouter
from .auth_router import router as auth_router
from .utilisateur_router import router as utilisateur_router
from .client_router import router as router_client
from .objet_router import router as router_objet
from .commande_router import router as router_commande
from .detail_commande_router import router as detail_commande_router
from .role_router import router as role_router
from .commune_router import router as commune_router

router = APIRouter(prefix="/api/v1")
router.include_router(router_client)
router.include_router(router_objet)
router.include_router(router_commande)
router.include_router(detail_commande_router)
router.include_router(auth_router)
router.include_router(utilisateur_router)
router.include_router(role_router)
router.include_router(commune_router)