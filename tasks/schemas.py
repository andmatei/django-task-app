from ninja import Schema
from typing import List
from typing import Optional

from ninja.orm import ModelSchema
from .models import Task

class TaskSchema(ModelSchema):
    class Meta:
        model = Task
        fields = "__all__"

class TaskIn(ModelSchema):
    class Meta:
        model = Task
        exclude = ["id"]

class TaskPageDataSchema(Schema):
    number: int
    num_pages: int
    has_next: bool
    has_previous: bool
    tasks: List[TaskSchema]

class TaskQueryParams(Schema):
    days_time_span: Optional[int] = 30
    tasks_per_page: Optional[int] = 10
    page_number: Optional[int] = 1
    priority_filter: Optional[int] = None
