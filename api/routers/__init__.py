from fastapi import APIRouter
from .auth_router import router as auth_router
from .utilisateur_router import router as utilisateur_router
from .client_router import router as router_client
from .commande_router import router as router_commande
from .detail_commande_router import router as detail_commande_router

router = APIRouter(prefix="/api/v1")
router.include_router(router_client)
router.include_router(router_commande)
router.include_router(detail_commande_router)
router.include_router(auth_router)
router.include_router(utilisateur_router)