from fastapi import APIRouter
from auth.apis.users import router as user_api


router= APIRouter()

router.include_router(router=user_api)
