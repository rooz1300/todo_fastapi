from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from core.database import get_db
from tasks.models import TaskModel
from tasks.schemas import TaskReturnSchema

router = APIRouter()

@router.get("/tasks/", tags=["tasks"], response_model=List[TaskReturnSchema])
async def retrieve_task_list(db: Session = Depends(get_db)):
    # .all() already returns a list, so return it directly
    results = db.query(TaskModel).all()
    print(f"Retrieved {len(results)} task(s) from the database.")
    return results  # <-- FIXED: Removed the extra []

@router.get("/tasks/{task_id}", tags=["tasks"], response_model=TaskReturnSchema)
async def retrieve_task(task_id: UUID, db: Session = Depends(get_db)):
    # Query for the specific task
    result = db.query(TaskModel).filter(TaskModel.id == task_id).first()
    
    # Return 404 if the task doesn't exist
    if not result:
        raise HTTPException(status_code=404, detail="Task not found")
    
    return result