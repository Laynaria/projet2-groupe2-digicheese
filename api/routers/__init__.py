from fastapi import APIRouter
from .client_router import router as router_client
from .objet_router import router as router_objet

router = APIRouter(prefix="/api/v1")
router.include_router(router_client)
router.include_router(router_objet)