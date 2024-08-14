# 2. Задайте переменные разных типов данных:
#   - Создайте переменную immutable_var и присвойте ей кортеж из нескольких элементов разных типов данных.
#   - Выполните операции вывода кортежа immutable_var на экран.
#
# 3. Изменение значений переменных:
#   - Попытайтесь изменить элементы кортежа immutable_var. Объясните, почему нельзя изменить значения элементов кортежа.
#
# 4. Создание изменяемых структур данных:
#   - Создайте переменную mutable_list и присвойте ей список из нескольких элементов.
#   - Измените элементы списка mutable_list.
#   - Выведите на экран измененный список mutable_list.

immutable_var = (1, 2.5, "Pavel", True, ["name", "age", "sex"])
print(immutable_var)
immutable_var[-1][:] = ["Pavel", 31, "male"]
print(immutable_var)

mutable_list = [1, 2.5, "Pavel", True, "a", "b", 7, 5]
print(mutable_list)
mutable_list[1] = "Name"
mutable_list[-4] = False
print(mutable_list)
