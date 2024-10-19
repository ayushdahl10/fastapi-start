from fastapi import APIRouter
from auth.apis.users import router as user_api
from auth.apis.login_register import router as auth_router
from auth.apis.permissions import router as perm_router
from web.api import router as setting_api
from todo.api import router as todo_router


router = APIRouter()

router.include_router(router=auth_router)
router.include_router(router=setting_api)
router.include_router(router=user_api)
router.include_router(router=perm_router)
router.include_router(router=todo_router)
