from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from api.database import get_db
from .. import models, schemas
from api.security import get_current_user, oauth2_scheme

router = APIRouter()

@router.post("/tasks/", response_model=schemas.Task)
async def create_task(
    task: schemas.TaskCreate,
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme)
):
    user = await get_current_user(db=db, token=token) 
    db_task = models.Task(**task.model_dump(), user_id=user.id) 
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

@router.get("/tasks/", response_model=List[schemas.Task])
async def read_tasks(
    skip: int = 0,
    limit: int = 10,
    status: Optional[str] = None,
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme)
):
    user = await get_current_user(db=db, token=token) 
    query = db.query(models.Task).filter(models.Task.user_id == user.id)
    
    if status:
        query = query.filter(models.Task.status == status)
    
    tasks = query.offset(skip).limit(limit).all()
    return tasks

@router.get("/tasks/{task_id}", response_model=schemas.Task)
async def read_task(
    task_id: int,
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme)
):
    user = await get_current_user(db=db, token=token) 
    task = db.query(models.Task).filter(
        models.Task.id == task_id,
        models.Task.user_id == user.id 
    ).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@router.put("/tasks/{task_id}", response_model=schemas.Task)
async def update_task(
    task_id: int,
    task_update: schemas.TaskUpdate,
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme)
):
    user = await get_current_user(db=db, token=token) 
    db_task = db.query(models.Task).filter(
        models.Task.id == task_id,
        models.Task.user_id == user.id
    ).first()
    
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    for field, value in task_update.model_dump(exclude_unset=True).items():
        setattr(db_task, field, value)
    
    db.commit()
    db.refresh(db_task)
    return db_task

@router.delete("/tasks/{task_id}")
async def delete_task(
    task_id: int,
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme)
):
    user = await get_current_user(db=db, token=token) 
    db_task = db.query(models.Task).filter(
        models.Task.id == task_id,
        models.Task.user_id == user.id  
    ).first()
    
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    db.delete(db_task)
    db.commit()
    return {"detail": "Task deleted"}