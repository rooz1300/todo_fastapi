from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from core.database import get_db
from tasks.models import TaskModel
from tasks.schemas import TaskReturnSchema, TaskCreateSchema, TaskUpdateSchema
from users.models import UserModel # Import User Model to verify existence

router = APIRouter(prefix="/tasks", tags=["tasks"])

@router.get("/", response_model=List[TaskReturnSchema])
async def retrieve_task_list(
    is_completed: bool = Query(default=None, description="the task is completed or not"),
    limit: int = Query(default=10, ge=1, le=50, description="the number of tasks to retrieve"),
    offset: int = Query(default=0, ge=0, description="the number of tasks to skip"),
    db: Session = Depends(get_db)
):
    results = db.query(TaskModel)
    if is_completed is not None:
        results = results.filter(TaskModel.is_completed == is_completed)
    
    # Apply pagination
    results = results.limit(limit).offset(offset).all()
    return results

@router.get("/{task_id}", response_model=TaskReturnSchema)
async def retrieve_task(task_id: UUID, db: Session = Depends(get_db)):
    result = db.query(TaskModel).filter(TaskModel.id == task_id).first()
    if not result:
        raise HTTPException(status_code=404, detail="Task not found")
    return result

@router.post("/", response_model=TaskReturnSchema, status_code=status.HTTP_201_CREATED)
async def create_new_task(request: TaskCreateSchema, db: Session = Depends(get_db)):
    # ⚠️ TEMPORARY LOGIC: 
    # In a real app, you would get the user_id from the JWT token (current_user.id).
    # For now, we assign it to the first user found in the DB, or ID 1.
    
    user = db.query(UserModel).first()
    if not user:
        raise HTTPException(status_code=400, detail="No users found. Please register a user first.")
    
    task_data = request.model_dump()
    task_data["user_id"] = user.id  # Inject the user_id here
    
    task_obj = TaskModel(**task_data)
    db.add(task_obj)
    db.commit()
    db.refresh(task_obj)
    return task_obj

@router.put("/{task_id}", response_model=TaskReturnSchema)
async def update_task(task_id: UUID, request: TaskUpdateSchema, db: Session = Depends(get_db)):
    task = db.query(TaskModel).filter(TaskModel.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    update_data = request.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(task, key, value)
        
    db.commit()
    db.refresh(task)
    return task

@router.patch("/{task_id}", response_model=TaskReturnSchema)
async def patch_task(task_id: UUID, request: TaskUpdateSchema, db: Session = Depends(get_db)):
    task = db.query(TaskModel).filter(TaskModel.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
        
    update_data = request.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(task, key, value)
        
    db.commit()
    db.refresh(task)
    return task

@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(task_id: UUID, db: Session = Depends(get_db)):
    task = db.query(TaskModel).filter(TaskModel.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
        
    db.delete(task)
    db.commit()
    return None