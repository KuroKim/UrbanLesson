# Задача "Имитация работы с БД":
# Создайте новое приложение FastAPI и сделайте CRUD запросы.
# Создайте словарь users = {'1': 'Имя: Example, возраст: 18'}
# Реализуйте 4 CRUD запроса:
# get запрос по маршруту '/users', который возвращает словарь users.
# post запрос по маршруту '/user/{username}/{age}', который добавляет в словарь по максимальному по значению ключом
# значение строки "Имя: {username}, возраст: {age}". И возвращает строку "User <user_id> is registered".
# put запрос по маршруту '/user/{user_id}/{username}/{age}', который обновляет значение из словаря users под ключом
# user_id на строку "Имя: {username}, возраст: {age}". И возвращает строку "The user <user_id> is updated"
# delete запрос по маршруту '/user/{user_id}', который удаляет из словаря users по ключу user_id пару.
# Выполните каждый из этих запросов по порядку. Ответы должны совпадать:
# 1. GET '/users'
# {
# "1": "Имя: Example, возраст: 18"
# }
# 2. POST '/user/{username}/{age}' # username - UrbanUser, age - 24
# "User 2 is registered"
# 3. POST '/user/{username}/{age}' # username - NewUser, age - 22
# "User 3 is registered"
# 4. PUT '/user/{user_id}/{username}/{age}' # user_id - 1, username - UrbanProfi, age - 28
# "User 1 has been updated"
# 5. DELETE '/user/{user_id}' # user_id - 2
# "User 2 has been deleted"
# 6. GET '/users'
# {
# "1": "Имя: UrbanProfi, возраст: 28",
# "3": "Имя: NewUser, возраст: 22"
# }
# Примечания:
# Не забудьте написать валидацию для каждого запроса, аналогично предыдущему заданию.


from fastapi import FastAPI, HTTPException, Path

app = FastAPI()

users = {'1': 'Имя: Example, возраст: 18'}


@app.get("/users")
def get_users():
    return users


@app.post("/user/{username}/{age}")
def add_user(
    username: str = Path(..., min_length=3, max_length=50, description="Имя пользователя", examples={"example": {"value": "UrbanUser"}}),
    age: int = Path(..., ge=1, le=120, description="Возраст пользователя, от 1 до 120", examples={"example": {"value": 25}})
):
    if age <= 0:
        raise HTTPException(status_code=400, detail="Возраст должен быть положительным числом.")

    new_id = str(max(map(int, users.keys())) + 1)
    users[new_id] = f"Имя: {username}, возраст: {age}"
    return f"User {new_id} is registered"


@app.put("/user/{user_id}/{username}/{age}")
def update_user(
    user_id: int = Path(..., ge=1, le=100, description="ID пользователя, от 1 до 100", examples={"example": {"value": 1}}),
    username: str = Path(..., min_length=3, max_length=50, description="Имя пользователя", examples={"example": {"value": "UrbanUpdated"}}),
    age: int = Path(..., ge=1, le=120, description="Возраст пользователя, от 1 до 120", examples={"example": {"value": 30}})
):
    user_id = str(user_id)
    if user_id not in users:
        raise HTTPException(status_code=404, detail="Пользователь с данным ID не найден.")
    users[user_id] = f"Имя: {username}, возраст: {age}"
    return f"The user {user_id} is updated"


@app.delete("/user/{user_id}")
def delete_user(
    user_id: int = Path(..., ge=1, le=100, description="ID пользователя, от 1 до 100", examples={"example": {"value": 1}})
):
    user_id = str(user_id)
    if user_id not in users:
        raise HTTPException(status_code=404, detail="Пользователь с данным ID не найден.")
    del users[user_id]
    return f"User {user_id} has been deleted"
