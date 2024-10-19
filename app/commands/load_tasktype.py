from sqlalchemy.orm import Session
import shortuuid

from manager.database import get_db
from todo.constant import TASK_TYPES, TaskStatus
from todo.models import TaskType


def load_tasktype():
    db: Session = next(get_db())
    for task in TASK_TYPES:
        task_data = TaskType(
            name=task,
            status=TaskStatus.in_progress,
            owner=0,
            is_default=True,
            uid=shortuuid.uuid(),
            created_by="superuser",
        )
        db.add(task_data)
        db.commit()
    print("Default task types created successfully")
