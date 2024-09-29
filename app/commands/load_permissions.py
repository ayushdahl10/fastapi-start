from fastapi import Depends
from sqlalchemy.orm import Session

from main import app
from auth import models,schemas
from services.role_perm import create_permissions, get_permission_by_name,delete_all_permissions
from manager.database import get_db
from .handle_permissions import load_default_permissions

def load_permissions():
    app_routes= app.routes
    db:Session= next(get_db())
    delete_all_permissions(db=db)
    for route in app_routes:
        get_permission= get_permission_by_name(db=db,name=str(route.name))
        if not get_permission:
            path=str(route.path)
            method=list(route.methods)[0]
            name= route.name
            perms= schemas.Permission(**{'url_path':str(route.path),'method':method,'name':name})
            create_permissions(db=db,permission=perms)
    print("permissions updated")
