from fastapi import APIRouter
from .client_router import router as router_client
from .commande_router import router as router_commande

router = APIRouter(prefix="/api/v1")
router.include_router(router_client)
router.include_router(router_commande)