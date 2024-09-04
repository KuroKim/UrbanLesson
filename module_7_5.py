# Цель задания:
#
# Освоить работу с файловой системой в Python, используя модуль os.
# Научиться применять методы os.walk, os.path.join, os.path.getmtime, os.path.dirname, os.path.getsize и использование модуля time для корректного отображения времени.
#
# Задание:
#
# Создайте новый проект или продолжите работу в текущем проекте.
# Используйте os.walk для обхода каталога, путь к которому указывает переменная directory
# Примените os.path.join для формирования полного пути к файлам.
# Используйте os.path.getmtime и модуль time для получения и отображения времени последнего изменения файла.
# Используйте os.path.getsize для получения размера файла.
# Используйте os.path.dirname для получения родительской директории файла.
# Так как в разных операционных системах разная схема расположения папок, тестировать проще всего в папке проекта (directory = “.”)
# Пример возможного вывода:
# Обнаружен файл: main.py, Путь: ./main.py, Размер: 111 байт, Время изменения: 11.11.1111 11:11, Родительская директория.


import os
import time


def get_file_info(directory):
    file_count = 0
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_count += 1
            file_path = os.path.join(root, file)
            file_size = os.path.getsize(file_path)
            last_modified = time.strftime("%d.%m.%Y %H:%M", time.localtime(os.path.getmtime(file_path)))
            parent_directory = os.path.dirname(file_path)
            print(f"Обнаружен файл: {file}, Путь: {file_path}, Размер: {file_size} байт, Время изменения: {last_modified}, Родительская директория: {parent_directory}")
    print(f"Всего обнаружено {file_count} файлов.")


directory = "."
get_file_info(directory)
