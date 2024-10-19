from enum import Enum
from typing_extensions import List


class ProjectStatus(str, Enum):
    pending = "pending"
    in_progress = "in_progress"
    completed = "completed"
    blocked = "blocked"
    cancel = "cancel"


class TaskStatus(str, Enum):
    pending = "pending"
    in_progress = "in_progress"
    in_review = "in_review"
    review_changes = "review_changes"
    completed = "completed"
    blocked = "blocked"


TASK_TYPES: List = [
    "MEETING",
    "GYM",
    "SHOPPING",
]
