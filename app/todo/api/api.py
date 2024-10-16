from fastapi import Depends,HTTPException,Request
from fastapi import APIRouter
from sqlalchemy.orm import Session
from starlette import status
from typing import List

from helpers.base_res import success_response
from manager.database import get_db
from auth.authentication import user_permission
from fastapi.security.api_key import APIKeyHeader
from helpers import base_service
from todo.models import Project, Task
from todo.schemas import  (
    ProjectDetail,
    ProjectCreate,
    TaskCreate,
    TaskDetail,
)

router=APIRouter()
api_key_header = APIKeyHeader(name='Authorization')
router.dependencies=[Depends(api_key_header)]

#project api starts here

@router.post("/project",tags=['Project'], response_model=ProjectDetail)
@user_permission
def create_project(request:Request,project:ProjectCreate ,db:Session=Depends(get_db)):
    project.owner=request.state.user.id
    project= base_service.save_model(db=db,validated_data=project,cls=Project)
    return project

@router.get("/project", tags=['Project'],response_model=List[ProjectDetail])
@user_permission
def get_project(request:Request, db:Session=Depends(get_db)):
    project_list= base_service.model_list(db=db,cls=Project)
    return project_list

@router.get("/project/{uid}",tags=['Project'], response_model=ProjectDetail)
@user_permission
def get_project_detail(request:Request,uid:str,db:Session= Depends(get_db)):
    project_detail= base_service.model_detail(cls=Project,uid=uid,db=db)
    if not project_detail:
        raise HTTPException(detail=f"object not found with uid= {uid}",status_code=status.HTTP_404_NOT_FOUND)
    return project_detail

@router.delete("/project/{uid}", tags=['Project'])
@user_permission
def delete_project(request:Request, uid:str, db:Session= Depends(get_db)):
    base_service.delete_model(cls=Project, uid=uid, force_delete=False,db=db)
    return success_response("data deleted successfully")

#project api ends here

#task api starts here

@router.post("/task", tags=['Task'], response_model=TaskDetail)
@user_permission
def create_task(request:Request, task:TaskCreate, db:Session=Depends(get_db)):
    project_id= base_service.model_detail(cls=Project,db=db,uid=task.project_id)
    if not project_id:
        raise HTTPException(detail=f"object not found with project uid= {task.project_id}")
    task.project_id=project_id.id
    task_obj= base_service.save_model(cls=Task, db=db,validated_data=task)
    return task_obj

@router.get("/task", tags=['Task'], response_model=List[TaskDetail])
@user_permission
def get_task(request:Request, db:Session=Depends(get_db)):
    model_list= base_service.model_list(db=db, cls= Task)
    return model_list

@router.get('/task/{uid}', tags=['Task'], response_model=TaskDetail)
@user_permission
def get_task_detail(request:Request, uid:str, db:Session=Depends(get_db)):
    task_obj= base_service.model_detail(cls=Task,uid=uid,db=db)
    if not task_obj:
        raise HTTPException(detail=f"object not found with uid= {uid}",status_code=status.HTTP_404_NOT_FOUND)
    return task_obj

@router.patch("/task", tags=['Task'])
@user_permission
def update_task(request:Request, uid:str,task:TaskCreate, db:Session=Depends(get_db)):
    ...

@router.delete("/task/{uid}", tags=['Task'])
@user_permission
def delete_task(request:Request, uid:str, db:Session=Depends(get_db)):
    return base_service.delete_model(cls=Task, uid=uid, force_delete=False, db=db)

#task api ends here
