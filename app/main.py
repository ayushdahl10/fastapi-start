from fastapi import FastAPI, APIRouter
from manager import engine

from auth import models

#import apis
from auth.apis import users,permissions


models.Base.metadata.create_all(bind=engine)

app=FastAPI(swagger_ui_parameters={"deepLinking": False})


app.include_router(users.router)
app.include_router(permissions.router)
