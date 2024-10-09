import matplotlib.pyplot as plt
import pandas as pd
from pathlib import Path
from PIL import Image
import multiprocessing as mp


def process_image(file_path):
    """Функция для обработки изображения: изменение размера и перевод в ЧБ"""
    try:
        image = Image.open(file_path)
        print("Изображение успешно открыто.")
    except IOError:
        print("Ошибка при открытии изображения.")
        return None

    # Получаем ширину и высоту изображения
    width, height = image.size
    print(f"Начальная ширина: {width}, начальная высота: {height}")

    # Уменьшаем изображение на 50%, сохраняя оригинал
    new_width = int(width / 2)
    new_height = int(height / 2)
    resized_image = image.resize((new_width, new_height))

    # Сохраняем измененное изображение
    resized_image.save(f'{file_path.stem}_resized.jpg')

    # Переводим итоговое изображение в ЧБ
    grayscale_image = resized_image.convert('L')
    grayscale_image.save(f'{file_path.stem}_grayscale.jpg')

    print("Изображение успешно обработано.")
    return grayscale_image


def plot_histogram(grayscale_image, file_name):
    """Функция для построения и сохранения гистограммы"""
    # Получаем данные пикселей черно-белого изображения
    pixel_data = grayscale_image.getdata()

    # Строим гистограмму
    plt.figure(figsize=(10, 6))
    plt.hist(pixel_data, bins=256, range=(0, 255), color='black', alpha=0.7)
    plt.title('Гистограмма черно-белого изображения')
    plt.xlabel('Яркость (уровни от 0 до 255)')
    plt.ylabel('Частота')
    plt.grid(True)

    # Сохраняем гистограмму в файл
    histogram_filename = f'{file_name}_histogram.png'
    plt.savefig(histogram_filename)
    print(f"Гистограмма сохранена как {histogram_filename}")

    # Закрываем фигуру
    plt.close()


def analyze_image_data(file_name):
    """Функция для анализа данных яркости изображения с использованием pandas"""
    # Открытие черно-белого изображения
    grayscale_image = Image.open(f'{file_name}_grayscale.jpg')

    # Получаем данные пикселей черно-белого изображения
    pixel_data = list(grayscale_image.getdata())

    # Создаем DataFrame с данными яркости пикселей
    df = pd.DataFrame(pixel_data, columns=['Brightness'])

    # Описательная статистика
    print(df.describe())

    # Создаем категории яркости
    bins = [0, 50, 100, 150, 200, 255]
    labels = ['0-50', '51-100', '101-150', '151-200', '201-255']

    df['Brightness Group'] = pd.cut(df['Brightness'], bins=bins, labels=labels, include_lowest=True)

    # Подсчет количества пикселей в каждой группе яркости
    brightness_group_distribution = df['Brightness Group'].value_counts().sort_index()

    print(brightness_group_distribution)


if __name__ == '__main__':
    current_dir = Path(__file__).parent
    file_path = current_dir / '03619.jpg'
    file_name = file_path.stem

    # Создаем процессы для параллельного выполнения задач
    with mp.Pool(processes=3) as pool:
        # 1. Процесс обработки изображения (resize и grayscale)
        grayscale_image = process_image(file_path)

        if grayscale_image:
            # 2. Процесс построения гистограммы
            pool.apply_async(plot_histogram, args=(grayscale_image, file_name))

            # 3. Процесс анализа данных с использованием pandas
            pool.apply_async(analyze_image_data, args=(file_name,))

        # Ждем завершения всех процессов
        pool.close()
        pool.join()
