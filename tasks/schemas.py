from ninja import Schema
from typing import List, Dict
from datetime import date, datetime
from typing import Optional

class TaskSchema(Schema):
    id: int
    user_email: str
    task: str
    due_by: datetime
    priority: int
    is_urgent: Optional[bool] = False


class CreateTaskSchema(Schema):
    user_email: str
    task: str
    due_by: datetime
    priority: int
    is_urgent: Optional[bool] = False

class UpdateTaskSchema(Schema):
    user_email: str
    task: str
    due_by: datetime
    priority: int
    is_urgent: Optional[bool] = False


class TaskPageSchema(Schema):
    number: int
    num_pages: int
    has_next: bool
    has_previous: bool
    tasks: List[TaskSchema]

class TaskStatsSchema(Schema):
    counts: Dict[str, int]
    dates: Dict[str, List[int]]

class TaskPageDataSchema(Schema):
    page: TaskPageSchema
    start_date: datetime
    end_date: datetime
    stats: TaskStatsSchema

class TaskQueryParams(Schema):
    days: Optional[int] = 30
    tasks_per_page: Optional[int] = 10
    page_number: Optional[int] = 1