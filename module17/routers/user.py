# В модуле user.py:
# Создайте новый маршрут get "/user_id/tasks" и функцию tasks_by_user_id. Логика этой функции должна заключатся в возврате всех Task конкретного User по id.
# Дополните функцию delete_user так, чтобы вместе с пользователем удалялись все записи связанные с ним.

from fastapi import APIRouter, Depends, status, HTTPException
# Сессия БД
from sqlalchemy.orm import Session
# Функция подключения к БД
from module17.backend.db_depends import get_db
# Аннотации, Модели БД и Pydantic.
from typing import Annotated
from module17.models import User, Task
from module17.schemas import CreateUser, UpdateUser
# Функции работы с записями.
from sqlalchemy import insert, select, update, delete
# Функция создания slug-строки
from slugify import slugify

router = APIRouter(prefix="/user", tags=["user"])


@router.get("/")
async def all_users(db: Annotated[Session, Depends(get_db)]):
    query = select(User)
    users = db.scalars(query).all()
    return users


@router.get("/user_id")
async def user_by_id(user_id: int, db: Annotated[Session, Depends(get_db)]):
    query = select(User).where(User.id == user_id)
    user = db.scalars(query).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User was not found")
    return user


@router.post("/create")
async def create_user(
    user: CreateUser,
    db: Annotated[Session, Depends(get_db)]
):
    user_slug = slugify(user.username)
    query = select(User).where(User.slug == user_slug)
    if db.scalars(query).first():
        raise HTTPException(status_code=400, detail="Username already exists")
    stmt = insert(User).values(
        username=user.username,
        firstname=user.firstname,
        lastname=user.lastname,
        age=user.age,
        slug=user_slug
    )
    db.execute(stmt)
    db.commit()
    return {'status_code': status.HTTP_201_CREATED, 'transaction': 'Successful'}


@router.put("/update/{user_id}")
async def update_user(
    user_id: int,
    user: UpdateUser,
    db: Annotated[Session, Depends(get_db)]
):
    query = select(User).where(User.id == user_id)
    if db.scalars(query).first() is None:
        raise HTTPException(status_code=404, detail="User was not found")
    stmt = update(User).where(User.id == user_id).values(
        firstname=user.firstname,
        lastname=user.lastname,
        age=user.age
    )
    db.execute(stmt)
    db.commit()
    return {'status_code': status.HTTP_200_OK, 'transaction': 'User update is successful!'}


@router.delete("/delete/{user_id}")
async def delete_user(
    user_id: int,
    db: Annotated[Session, Depends(get_db)]
):
    query = select(User).where(User.id == user_id)
    if db.scalars(query).first() is None:
        raise HTTPException(status_code=404, detail="User was not found")

    delete_tasks = delete(Task).where(Task.user_id == user_id)
    db.execute(delete_tasks)

    stmt = delete(User).where(User.id == user_id)
    db.execute(stmt)
    db.commit()
    return {'status_code': status.HTTP_200_OK, 'transaction': 'User deletion is successful!'}


@router.get("/user_id/tasks")
async def tasks_by_user_id(
        user_id: int,
        db: Annotated[Session, Depends(get_db)]
):
    query = select(User).join(User.tasks).where(User.id == user_id)
    user = db.scalars(query).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User was not found")

    tasks_query = select(Task).where(Task.user_id == user_id)
    tasks = db.scalars(tasks_query).all()
    return user.tasks
