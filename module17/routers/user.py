# Напишите логику работы функций маршрутов:
# Каждая из нижеперечисленных функций подключается к базе данных в момент обращения при помощи функции
# get_db - Annotated[Session, Depends(get_db)]
# Функция all_users ('/'):
# Должна возвращать список всех пользователей из БД. Используйте scalars, select и all
# Функция user_by_id ('/user_id'):
# Для извлечения записи используйте ранее импортированную функцию select.
# Дополнительно принимает user_id.
# Выбирает одного пользователя из БД.
# Если пользователь не None, то возвращает его.
# В противном случае выбрасывает исключение с кодом 404 и описанием "User was not found"
# Функция craete_user ('/create'):
# Для добавления используйте ранее импортированную функцию insert.
# Дополнительно принимает модель CreateUser.
# Подставляет в таблицу User запись значениями указанными в CreateUser.
# В конце возвращает словарь {'status_code': status.HTTP_201_CREATED, 'transaction': 'Successful'}
# Обработку исключения существующего пользователя по user_id или username можете сделать по желанию.
# Функция update_user ('/update'):
# Для обновления используйте ранее импортированную функцию update.
# Дополнительно принимает модель UpdateUser и user_id.
# Если находит пользователя с user_id, то заменяет эту запись значениям из модели UpdateUser. Далее возвращает словарь
# {'status_code': status.HTTP_200_OK, 'transaction': 'User update is successful!'}
# В противном случае выбрасывает исключение с кодом 404 и описанием "User was not found"
# Функция delete_user ('/delete'):
# Для удаления используйте ранее импортированную функцию delete.
# Всё должно работать аналогично функции update_user, только объект удаляется.
# Исключение выбрасывать то же.
# Создайте, измените и удалите записи через интерфейс Swagger:
# Создайте 3 записи User с соответствующими параметрами:
# username: user1, user2, user3
# firstname: Pasha, Roza, Alex
# lastname: Technique, Syabitova, Unknown
# age: 40, 62, 25
# Измените запись с id=3: firstname = Bear, lastname = Grylls, age = 50
# Удалите запись с id =2.
# Выведите всех пользователей.
# Проверьте, выбрасываются ли исключения в ваших запросах.

from fastapi import APIRouter, Depends, status, HTTPException
# Сессия БД
from sqlalchemy.orm import Session
# Функция подключения к БД
from module17.backend.db_depends import get_db
# Аннотации, Модели БД и Pydantic.
from typing import Annotated
from module17.models import User
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
    stmt = delete(User).where(User.id == user_id)
    db.execute(stmt)
    db.commit()
    return {'status_code': status.HTTP_200_OK, 'transaction': 'User deletion is successful!'}
