
from passlib.utils.decor import print_function
from typing_extensions import List

from manager.database import get_db
from auth import models, schemas
from services.role_perm import (
            update_roles_with_permissions,
            get_permission_by_name,
            check_permission,
            get_role_by_name,
            remove_role_permission,
        )



USER_PERMISSIONS=[
    ('get_users','get'),
    ('get_user_by_id','get'),
    ('read_users_me','get'),
]

ROLE_PERMISSIONS=[
    ("get_all_roles",'get'),
    ("get_role_by_id",'get'),
]


#creating a default permissions
def admin_permissions()->List:
    return{
        'name':'Admin',
        'permissions':[
            USER_PERMISSIONS,
            ROLE_PERMISSIONS,
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
        name= role.get('name')
        role_instance=get_role_by_name(db=db,role_name=role.get('name').lower())
        permissions= role.get('permissions')
        permission_id:list=[]
        remove_role_permission(db=db)
        for permission in permissions:
            for p in permission:
                print(p)
                perm_name=p[0]
                permission_instance=get_permission_by_name(db=db,name=perm_name)
                print(role_instance)
                role_perm_exists= check_permission(db=db,role_id=role_instance.id,permission_id=permission_instance.id)
                if role_perm_exists==False:
                    permission_id.append(permission_instance.uid)
        if permission_id:
            update_roles_with_permissions(db=db,permissions=permission_id,role_name=role.get('name'))
            print("permission updated successfully")
            return
        print("permission already upto date")
        # update_roles_with_permissions(db=db,)
