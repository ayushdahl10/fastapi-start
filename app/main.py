from fastapi import FastAPI, Request
from starlette.middleware import Middleware
from starlette.types import Send,Receive,Scope
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.authentication import AuthenticationMiddleware
import time

from manager import engine
from auth import models
#importing api routes
from auth.apis import users,permissions,login_register

models.Base.metadata.create_all(bind=engine)
app=FastAPI(swagger_ui_parameters={"deepLinking": False})

origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:8000",
]

#add middlewares
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(login_register.router)
app.include_router(users.router)
app.include_router(permissions.router)
