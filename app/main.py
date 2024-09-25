from fastapi import FastAPI, Request
from starlette.types import Send,Receive,Scope
from manager import engine

from auth import models

#import apis
from auth.apis import users,permissions,login_register


models.Base.metadata.create_all(bind=engine)

app=FastAPI(swagger_ui_parameters={"deepLinking": False})




app.include_router(login_register.router)
app.include_router(users.router)
app.include_router(permissions.router)

