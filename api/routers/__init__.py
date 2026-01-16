from fastapi import APIRouter
from .auth_router import router as auth_router
from .utilisateur_router import router as utilisateur_router
from .client_router import router as router_client
from .commande_router import router as router_commande
from .conditionnement_router import router as router_conditionnement
from .detail_commande_router import router as router_detail_commande

router = APIRouter(prefix="/api/v1")
router.include_router(router_client)
router.include_router(router_commande)
router.include_router(router_conditionnement)
router.include_router(router_detail_commande)
router.include_router(auth_router)
router.include_router(utilisateur_router)