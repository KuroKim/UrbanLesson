# Задание:
# Необходимо создать функцию, которая принимает объект (любого типа) в качестве аргумента и проводит интроспекцию этого
# объекта, чтобы определить его тип, атрибуты, методы, модуль, и другие свойства.
#
# 1. Создайте функцию introspection_info(obj), которая принимает объект obj.
# 2. Используйте встроенные функции и методы интроспекции Python для получения информации о переданном объекте.
# 3. Верните словарь или строки с данными об объекте, включающий следующую информацию:
#   - Тип объекта.
#   - Атрибуты объекта.
#   - Методы объекта.
#   - Модуль, к которому объект принадлежит.
#   - Другие интересные свойства объекта, учитывая его тип (по желанию).


def introspection_info(obj):
    info = {}

    info['type'] = type(obj).__name__

    attributes = [attr for attr in dir(obj) if not callable(getattr(obj, attr))]
    info['attributes'] = attributes

    methods = [method for method in dir(obj) if callable(getattr(obj, method))]
    info['methods'] = methods

    info['module'] = getattr(obj, '__module__', 'Модуль не определён')

    if isinstance(obj, (int, float, str, bool)):
        info['value'] = obj

    if isinstance(obj, (list, tuple, set)):
        info['length'] = len(obj)

    if isinstance(obj, dict):
        info['keys'] = list(obj.keys())

    return info


# Пример использования
class ExampleClass:
    def __init__(self, value):
        self.value = value

    def example_method(self):
        return self.value * 2


example_obj = ExampleClass(10)
print(introspection_info(example_obj))

number_info = introspection_info(42)
print(number_info)

string_info = introspection_info("hello world")
print(string_info)

list_info = introspection_info([1, 2, 3, 4])
print(list_info)

dict_info = introspection_info({'a': 1, 'b': 2})
print(dict_info)
