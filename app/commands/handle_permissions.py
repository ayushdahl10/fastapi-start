
from typing_extensions import List

from manager.database import get_db
from auth import models, schemas
from services.role_perm import update_roles_with_permissions


USER_PERMISSIONS=[
    ('create_user_admin','post'),
    ('get_users','get'),
    ('get_user_by_id','get'),
]

ROLE_PERMISSIONS=[

]


#creating a default permissions
def admin_permissions()->List:
    return{
        'name':'Admin',
        'permissions':[
            USER_PERMISSIONS,
        ]
    }




#add all the functions for permissions
def load_default_permissions():
    db:Session=next(get_db())
    roles:list=[
        admin_permissions(),
    ]
    #add permissions to roles
    for role in roles:
        permissions= role.get('permissions')
        for permission in permissions:
            print(permission[0])
        # update_roles_with_permissions(db=db,)
