# Задание "Раз, два, три, четыре, пять .... Это не всё?":
# Наши студенты, без исключения, - очень умные ребята. Настолько умные, что иногда по утру сами путаются в том, что намудрили вчера вечером.
# Один из таких учеников уснул на клавиатуре в процессе упорной учёбы (ещё и трудолюбивые). Тем не менее, даже после сна, его код остался рабочим и выглядел следующим образом:
#
# data_structure = [
#   [1, 2, 3],
#   {'a': 4, 'b': 5},
#   (6, {'cube': 7, 'drum': 8}),
#   "Hello",
#   ((), [{(2, 'Urban', ('Urban2', 35))}])
# ]
#
# Увидев это студент задался вопросом: "А есть ли универсальное решение для подсчёта суммы всех чисел и длин всех строк?"
# Да, выглядит страшно, да и обращаться нужно к каждой внутренней структуре (списку, словарю и т.д.) по-разному.
#
# Ученику пришлось каждый раз использовать индексацию и обращение по ключам - универсального решения для таких структур он не нашёл.
#
# Помогите сокурснику осуществить его задумку.
#
# Что должно быть подсчитано:
# Все числа (не важно, являются они ключами или значениям или ещё чем-то).
# Все строки (не важно, являются они ключами или значениям или ещё чем-то)


def calculate_structure_sum(data):
    total_sum = 0
    total_length = 0

    if isinstance(data, (int, float)):
        total_sum += data
    elif isinstance(data, str):
        total_length += len(data)
    elif isinstance(data, (list, tuple, set)):
        for item in data:
            total_sum += calculate_structure_sum(item)
    elif isinstance(data, dict):
        for key, value in data.items():
            total_sum += calculate_structure_sum(key)
            total_sum += calculate_structure_sum(value)

    return total_sum + total_length


# Пример использования:
data_structure = [
    [1, 2, 3],
    {'a': 4, 'b': 5},
    (6, {'cube': 7, 'drum': 8}),
    "Hello",
    ((), [{(2, 'Urban', ('Urban2', 35))}])
]

result = calculate_structure_sum(data_structure)
print(result)
