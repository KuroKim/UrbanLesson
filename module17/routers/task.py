# В модуле task.py:
# Функция all_tasks ('/') - идентично all_users.
# Функция task_by_id ('/task_id') - идентично user_by_id (тоже по id)
# Функция craete_task ('/create'):
# Дополнительно принимает модель CreateTask и user_id.
# Подставляет в таблицу Task запись значениями указанными в CreateUser и user_id, если пользователь найден.
# Т.е. при создании записи Task вам необходимо связать её с конкретным пользователем User.
# В конце возвращает словарь {'status_code': status.HTTP_201_CREATED, 'transaction': 'Successful'}
# В случае отсутствия пользователя выбрасывает исключение с кодом 404 и описанием "User was not found"
# Функция update_task ('/update') - идентично update_user.
# Функция delete_task ('/delete') - идентично delete_user.

from fastapi import APIRouter, Depends, status, HTTPException
# Сессия БД
from sqlalchemy.orm import Session
# Функция подключения к БД
from module17.backend.db_depends import get_db
# Аннотации, Модели БД и Pydantic.
from typing import Annotated
from module17.models import Task, User
from module17.schemas import CreateTask, UpdateTask
# Функции работы с записями.
from sqlalchemy import insert, select, update, delete
# Функция создания slug-строки
from slugify import slugify

router = APIRouter(prefix="/task", tags=["task"])


@router.get("/")
async def all_tasks(db: Annotated[Session, Depends(get_db)]):
    query = select(Task)
    tasks = db.scalars(query).all()
    return tasks


@router.get("/{task_id}")
async def task_by_id(task_id: int, db: Annotated[Session, Depends(get_db)]):
    query = select(Task).where(Task.id == task_id)
    task = db.scalars(query).first()
    if task is None:
        raise HTTPException(status_code=404, detail="Task was not found")
    return task


@router.post('/create')
async def create_task(
    task: CreateTask,
    user_id: int,
    db: Annotated[Session, Depends(get_db)]
):
    user_query = select(User).where(User.id == user_id)
    user = db.scalars(user_query).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User was not found")

    slug = slugify(task.title)
    stmt = insert(Task).values(
        title=task.title,
        content=task.content,
        priority=task.priority,
        completed=False,
        user_id=user_id,
        slug=slug
    )
    db.execute(stmt)
    db.commit()
    return {'status_code': status.HTTP_201_CREATED, 'transaction': 'Successful'}


@router.put("/update/{task_id}")
async def update_task(
    task_id: int,
    task: UpdateTask,
    db: Annotated[Session, Depends(get_db)]
):
    query = select(Task).where(Task.id == task_id)
    if db.scalars(query).first() is None:
        raise HTTPException(status_code=404, detail="Task was not found")

    stmt = update(Task).where(Task.id == task_id).values(
        title=task.title,
        content=task.content,
        priority=task.priority,
        completed=task.completed
    )
    db.execute(stmt)
    db.commit()
    return {'status_code': status.HTTP_200_OK, 'transaction': 'Task update is successful!'}


@router.delete("/delete/{task_id}")
async def delete_task(
    task_id: int,
    db: Annotated[Session, Depends(get_db)]
):
    query = select(Task).where(Task.id == task_id)
    if db.scalars(query).first() is None:
        raise HTTPException(status_code=404, detail="Task was not found")

    stmt = delete(Task).where(Task.id == task_id)
    db.execute(stmt)
    db.commit()
    return {'status_code': status.HTTP_200_OK, 'transaction': 'Task deletion is successful!'}
