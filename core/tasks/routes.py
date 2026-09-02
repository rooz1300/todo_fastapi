from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from core.database import get_db
from tasks.models import TaskModel
from tasks.schemas import TaskReturnSchema


router = APIRouter()



@router.get("/tasks/", tags=["tasks"], response_model=List[TaskReturnSchema])
async def retrieve_task_list(db:Session = Depends(get_db)):
    results = db.query(TaskModel).all()
    return [result for result in results]