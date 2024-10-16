from enum import Enum

class ProjectStatus(str, Enum):
    pending= 'pending'
    in_progress = 'in_progress'
    completed = 'completed'
    blocked= 'blocked'

class TaskStatus(str, Enum):
    pending= 'pending'
    in_progress = 'in_progress'
    completed = 'completed'
    blocked= 'blocked'

