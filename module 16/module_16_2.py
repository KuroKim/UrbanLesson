# Задача "Аннотация и валидация":
# Допишите валидацию для маршрутов из предыдущей задачи при помощи классов Path и Annotated:
# '/user/{user_id}' - функция, выполняемая по этому маршруту, принимает аргумент user_id, для которого необходимо написать следующую валидацию:
# Должно быть целым числом
# Ограничено по значению: больше или равно 1 и меньше либо равно 100.
# Описание - 'Enter User ID'
# Пример - '1' (можете подставить свой пример не противоречащий валидации)
# '/user' замените на '/user/{username}/{age}' - функция, выполняемая по этому маршруту, принимает аргументы username и age, для которых необходимо написать следующую валидацию:
# username - строка, age - целое число.
# username ограничение по длине: больше или равно 5 и меньше либо равно 20.
# age ограничение по значению: больше или равно 18 и меньше либо равно 120.
# Описания для username и age - 'Enter username' и 'Enter age' соответственно.
# Примеры для username и age - 'UrbanUser' и '24' соответственно. (можете подставить свои примеры не противоречащие валидации).
# Примечания:
# Если у вас не отображаются параметры Path, проверьте, сделали вы присвоение данных или подсказку типа. Верно: username: Annotated[...]. Не верно: username = Annotated[...]

from typing import Annotated
from fastapi import FastAPI, Path

app = FastAPI()

@app.get("/user/{user_id}")
async def read_user_by_id(
    user_id: Annotated[
        int,
        Path(
            ...,  # Обязательный параметр
            description="Введите ID пользователя",
            ge=1,  # Минимум 1
            le=100,  # Максимум 100
            examples={"example_1": {"summary": "Valid ID", "value": 1}},
        ),
    ]
):
    return {"user_id": user_id}


@app.get("/user/{username}/{age}")
async def read_user_info(
    username: Annotated[
        str,
        Path(
            ...,  # Обязательный параметр
            description="Введите имя пользователя",
            min_length=5,  # Минимальная длина 5 символов
            max_length=20,  # Максимальная длина 20 символов
            examples={
                "example_username": {"summary": "Valid username", "value": "UrbanUser"}
            },
        ),
    ],
    age: Annotated[
        int,
        Path(
            ...,  # Обязательный параметр
            description="Введите возраст",
            ge=18,  # Минимум 18
            le=120,  # Максимум 120
            examples={"example_age": {"summary": "Valid age", "value": 24}},
        ),
    ]
):
    return {"username": username, "age": age}
