from typing import List
from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from api.database import get_db
from api.models import Task
from api.schemas import TaskCreate, TaskResponse, TaskUpdate

router = APIRouter(prefix="/api/tasks", tags=["tasks"])

@router.get("", response_model=List[TaskResponse])
def list_tasks(db: Session = Depends(get_db)):
    """Retorna todas as tarefas ordenadas por status (ativas primeiro) e data de criação decrescente."""
    return db.query(Task).order_by(Task.is_completed.asc(), Task.created_at.desc()).all()

@router.post("", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def create_task(task_in: TaskCreate, db: Session = Depends(get_db)):
    """Cria uma nova tarefa na lista."""
    new_task = Task(title=task_in.title)
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task

@router.patch("/{task_id}", response_model=TaskResponse)
def update_task(task_id: int, task_in: TaskUpdate, db: Session = Depends(get_db)):
    """Atualiza o estado de conclusão ou o título de uma tarefa existente."""
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Tarefa com ID {task_id} não encontrada."
        )

    if task_in.title is not None:
        task.title = task_in.title
    if task_in.is_completed is not None:
        task.is_completed = task_in.is_completed

    db.commit()
    db.refresh(task)
    return task

@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: int, db: Session = Depends(get_db)):
    """Remove uma tarefa da lista permanentemente."""
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Tarefa com ID {task_id} não encontrada."
        )

    db.delete(task)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
