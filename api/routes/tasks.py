from fastapi import APIRouter, Depends, HTTPException, Request
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


@router.get("/tasks/", response_model=schemas.PaginatedTasks)
async def read_tasks(
    request: Request,
    page: int = 1,
    size: int = 10,
    status: Optional[str] = None,
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme)
):
    user = await get_current_user(db=db, token=token)
    query = db.query(models.Task).filter(models.Task.user_id == user.id)

    if status:
        query = query.filter(models.Task.status == status)

    total_tasks = query.count()
    total_pages = (total_tasks + size - 1) // size
    tasks = query.order_by(models.Task.created_at.desc())\
        .offset((page - 1) * size)\
        .limit(size)\
        .all()

    tasks_dict = []
    for task in tasks:
        task_dict = {
            "id": task.id,
            "title": task.title,
            "description": task.description,
            "status": task.status,
            "created_at": task.created_at,
            "updated_at": task.updated_at,
            "user_id": task.user_id
        }
        tasks_dict.append(task_dict)

    base_url = str(request.url).split('?')[0]
    next_page = f"{base_url}?page={
        page + 1}&size={size}" if page < total_pages else None
    previous_page = f"{base_url}?page={
        page - 1}&size={size}" if page > 1 else None

    return schemas.PaginatedTasks(
        data=tasks_dict,
        current_page=page,
        total_pages=total_pages,
        next=next_page,
        previous=previous_page
    )


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
