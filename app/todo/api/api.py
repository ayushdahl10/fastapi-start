import datetime
from fastapi import Depends, HTTPException, Request, APIRouter, Form
from sqlalchemy.orm import Session
from starlette import status
from typing_extensions import List, Annotated

from helpers.base_res import success_response
from manager.database import get_db
from auth.authentication import user_permission
from fastapi.security.api_key import APIKeyHeader
from helpers import base_service
from todo.models import TaskType, Task
from todo.schemas import (
    TaskTypeDetail,
    TaskTypeCreate,
    TaskDetail,
    TaskCreateForm,
)

router = APIRouter()
api_key_header = APIKeyHeader(name="Authorization")
router.dependencies = [Depends(api_key_header)]


# project api starts here
@router.post("/task-type", tags=["Task Type"], response_model=TaskTypeDetail)
@user_permission
def create_task_type(
    request: Request,
    project: Annotated[TaskTypeCreate, Depends()],
    db: Session = Depends(get_db),
):
    project.owner = request.state.user.id
    project = base_service.save_model(db=db, validated_data=project, cls=TaskType)
    return project


@router.get("/task-type", tags=["Task Type"], response_model=List[TaskTypeDetail])
@user_permission
def get_task_type(request: Request, db: Session = Depends(get_db)):
    project_list = base_service.model_list(db=db, cls=TaskType).where(
        (TaskType.owner == request.state.user.id) | (TaskType.is_default)
    )
    return project_list


@router.delete("/task-type/{uid}", tags=["Task Type"])
@user_permission
def delete_task_type(request: Request, uid: str, db: Session = Depends(get_db)):
    base_service.delete_model(cls=TaskType, uid=uid, force_delete=False, db=db)
    return success_response("data deleted successfully")


# project api ends here


# task api starts here
@router.post("/task", tags=["Task"], response_model=TaskDetail)
@user_permission
def create_task(
    request: Request,
    task: Annotated[TaskCreateForm, Depends()],
    db: Session = Depends(get_db),
):
    if not task.is_everyday and task.end_datetime == "":
        raise HTTPException(
            detail="please select end date if you dont wanna set the task everyday",
            status_code=400,
        )
    if task.is_everyday:
        task.end_datetime = None
    task.start_datetime = datetime.datetime.strptime(
        task.start_datetime, "%y-%m-%d %H:%M:%S"
    )
    if task.end_datetime is not None:
        task.end_datetime = datetime.datetime.strptime(
            task.end_datetime, "%y-%m%d %H:%M:%S"
        )
    project_id = base_service.model_detail(cls=TaskType, db=db, uid=task.tasktype_id)
    if not project_id:
        raise HTTPException(
            detail=f"object not found with project uid= {task.tasktype_id}",
            status_code=status.HTTP_404_NOT_FOUND,
        )
    task.tasktype_id = project_id.id
    task_obj = base_service.save_model(cls=Task, db=db, validated_data=task)
    return task_obj


@router.get("/task", tags=["Task"], response_model=List[TaskDetail])
@user_permission
def get_task(
    request: Request, status: str, task_type_id: str, db: Session = Depends(get_db)
):
    model_list = (
        base_service.model_list(db=db, cls=Task)
        .join(Task.task_type)
        .filter(
            TaskType.uid == task_type_id,
            Task.status == status,
        )
    )
    return model_list


@router.get("/task/{uid}", tags=["Task"], response_model=TaskDetail)
@user_permission
def get_task_detail(request: Request, uid: str, db: Session = Depends(get_db)):
    task_obj = base_service.model_detail(cls=Task, uid=uid, db=db)
    if not task_obj:
        raise HTTPException(
            detail=f"object not found with uid= {uid}",
            status_code=status.HTTP_404_NOT_FOUND,
        )
    return task_obj


@router.patch("/task", tags=["Task"], response_model=TaskDetail)
@user_permission
def update_task(
    request: Request, uid: str, task: TaskCreateForm, db: Session = Depends(get_db)
):
    instance = base_service.model_detail(cls=Task, db=db, uid=uid)
    if not instance:
        raise HTTPException(
            detail=f"object doesnt not exists with uid= {uid}",
            status_code=status.HTTP_404_NOT_FOUND,
        )
    updated_task = base_service.update_model(
        db=db, update_payload=task, instance=instance, cls=Task
    )
    return updated_task


@router.delete("/task/{uid}", tags=["Task"])
@user_permission
def delete_task(request: Request, uid: str, db: Session = Depends(get_db)):
    base_service.delete_model(cls=Task, uid=uid, force_delete=False, db=db)
    return success_response(
        content="data deleted successfully",
        status_code=status.HTTP_200_OK,
    )


# task api ends here
