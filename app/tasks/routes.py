from fastapi import APIRouter, Path, Depends, HTTPException, Query
from fastapi.responses import JSONResponse
from typing import List

from tasks.schemas import (
    TaskCreateSchema, TaskUpdateSchema, TaskResponseSchema
)
from tasks.models import TaskModel
from sqlalchemy.orm import Session
from core.database import get_db

router = APIRouter(tags=["tasks"], prefix="/todo")


@router.get("/tasks", response_model=List[TaskResponseSchema])
async def get_tasks_list(completed: bool = Query(None, description="filter tasks base on is_completed"),
                         limit: int = Query(10,gt=0,le=100, description="max number of tasks"),
                         offset: int = Query(0,ge=0,description="pagination based on items"),
                         db: Session = Depends(get_db)):

    query = db.query(TaskModel)

    if completed:
        query = query.filter_by(is_completed=completed)

    return query.limit(limit).offset(offset).all()


@router.get("/tasks/{task_id}", response_model=TaskResponseSchema)
async def get_task(task_id: int = Path(..., gt=0), db: Session = Depends(get_db)):
    result = db.query(TaskModel).filter_by(id=task_id).one_or_none()
    if result:
        return result
    raise HTTPException(status_code=404, detail="Task not found")


@router.put("/tasks/{task_id}", response_model=TaskResponseSchema)
async def update_task(request: TaskUpdateSchema, task_id: int = Path(..., gt=0), db: Session = Depends(get_db)):
    task_obj = db.query(TaskModel).filter_by(id=task_id).one_or_none()
    if task_obj:
        for field, value in request.model_dump().items():
            setattr(task_obj, field, value)

        db.commit()
        db.refresh(task_obj)

        return task_obj

    raise HTTPException(status_code=404, detail="Task not found")


@router.post("/tasks/")
async def create_task(request: TaskCreateSchema, db: Session = Depends(get_db)):
    task_obj = TaskModel(**request.model_dump())
    db.add(task_obj)
    db.commit()
    db.refresh(task_obj)
    return task_obj


@router.delete("/tasks/{task_id}", status_code=204)
async def delete_task(task_id: int = Path(..., gt=0), db: Session = Depends(get_db)):
    task_obj = db.query(TaskModel).filter_by(id=task_id).one_or_none()
    if task_obj:
        db.delete(task_obj)
        db.commit()

        return JSONResponse(status_code=204, content={"message": "Task deleted"})

    raise HTTPException(status_code=404, detail="Task not found")
