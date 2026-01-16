from fastapi import APIRouter
from .auth_router import router as auth_router
from .utilisateur_router import router as utilisateur_router
from .client_router import router as router_client

router = APIRouter(prefix="/api/v1")
router.include_router(router_client)
router.include_router(auth_router)
router.include_router(utilisateur_router)
