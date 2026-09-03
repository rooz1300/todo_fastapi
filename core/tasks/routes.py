from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from core.database import get_db
from tasks.models import TaskModel
from tasks.schemas import TaskReturnSchema ,TaskCreateSchema, TaskUpdateSchema

router = APIRouter()

@router.get("/tasks/", response_model=List[TaskReturnSchema])
async def retrieve_task_list(
    Is_Completed: bool =Query(default=None,description="the task is completed or not"),
    limt: int = Query(default=10, ge=0 ,le=50, description="the number of tasks to retrieve"),
    offset: int = Query(default=0, ge=0, description="the number of tasks to skip"),
    db: Session = Depends(get_db)):
    # .all() already returns a list, so return it directly
    results = db.query(TaskModel)
    if Is_Completed is not None:
        results= results.filter_by( is_completed=Is_Completed)
        print(f"Retrieved {len(results.all())} task(s) from the database.")
    results = results.limit(limt).offset(offset)



    
    return results.all() 

@router.get("/tasks/{task_id}", response_model=TaskReturnSchema)
async def retrieve_task(task_id: UUID, db: Session = Depends(get_db)):
    # Query for the specific task
    result = db.query(TaskModel).filter(TaskModel.id == task_id).first()
    
    # Return 404 if the task doesn't exist
    if not result:
        raise HTTPException(status_code=404, detail="Task not found")
    
    return result

@router.post("/tasks",response_model=TaskReturnSchema)
async def create_new_task(request:TaskCreateSchema ,db: Session =  Depends(get_db)):
    # ** unpack the request data into the TaskModel constructor
    task_obj= TaskModel(**request.model_dump())
    db.add(task_obj)
    db.commit()
    db.refresh(task_obj)
    return task_obj

@router.put("/tasks/{task_id}", response_model=TaskReturnSchema)
async def update_task(task_id: UUID, request: TaskUpdateSchema, db: Session = Depends(get_db)):
    # Get the task from database
    task = db.query(TaskModel).filter(TaskModel.id == task_id).first()
    
    # Check if task exists
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    # Update only the fields that are provided (not None)
    update_data = request.model_dump(exclude_unset=True)  # For Pydantic v2
    # OR use request.dict(exclude_unset=True) for Pydantic v1
    
    for key, value in update_data.items():
        setattr(task, key, value)
    
    # Commit changes to database
    db.commit()
    db.refresh(task)
    
    return task


@router.delete("/tasks/{task_id}", response_model=dict)
async def delete_task(task_id: UUID, db: Session = Depends(get_db)):
    # Get the task from database
    task = db.query(TaskModel).filter(TaskModel.id == task_id).first()
    
    # Check if task exists
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    # Delete the task
    db.delete(task)
    db.commit()
    
    return {"message": f"Task with id {task_id} successfully deleted"}



@router.patch("/tasks/{task_id}", response_model=TaskReturnSchema)
async def patch_task(task_id: UUID, request: TaskUpdateSchema, db: Session = Depends(get_db)):
    # Get the task from database
    task = db.query(TaskModel).filter(TaskModel.id == task_id).first()
    
    # Check if task exists
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    # Get only the fields that were provided in the request
    update_data = request.model_dump(exclude_unset=True)  # For Pydantic v2
    # Update only the provided fields
    for key, value in update_data.items():
        setattr(task, key, value)
    
    # Commit changes to database
    db.commit()
    db.refresh(task)
    
    return task