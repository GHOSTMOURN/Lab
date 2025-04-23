import datetime
import tkinter as tk
from tkinter import ttk
import os

# Классы для измерений
class Measurement:
    """Базовый класс для хранения данных об измерении."""
    def __init__(self, date, place):
        self.date = datetime.datetime.strptime(date, "%Y.%m.%d").date()
        self.place = place.strip('"')

    def __str__(self):
        return f"Дата: {self.date}, Место: {self.place}"


class TemperatureMeasurement(Measurement):
    """Класс для измерения температуры и влажности."""
    def __init__(self, date, place, temperature, humidity):
        super().__init__(date, place)
        self.temperature = float(temperature)
        self.humidity = float(humidity)

    def __str__(self):
        return (f"{super().__str__()}, Температура: {self.temperature:.2f}°C, "
                f"Влажность: {self.humidity:.2f}%")


class PressureMeasurement(Measurement):
    """Класс для измерения давления."""
    def __init__(self, date, place, pressure):
        
        super().__init__(date, place)
        self.pressure = float(pressure)

    def __str__(self):
        return f"{super().__str__()}, Давление: {self.pressure:.2f} мм рт. ст."


# Функции для работы с данными
def parse_line(line):
    """Создаёт объект измерения из строки."""
    parts = line.strip().split()
    measurement_type = parts[0]

    if measurement_type == "temperature":
        return TemperatureMeasurement(parts[1], parts[2], parts[3], parts[4])
    elif measurement_type == "pressure":
        return PressureMeasurement(parts[1], parts[2], parts[3])
    else:
        raise ValueError("Неизвестный тип измерения")


def read_measurements_from_file(filename):
    """Читает измерения из файла и возвращает список объектов."""
    measurements = []
    if os.path.exists(filename):
        with open(filename, "r") as file:
            for line in file:
                if line.strip():  # Пропускаем пустые строки
                    measurement = parse_line(line)
                    measurements.append(measurement)
    return measurements


# Функции для интерфейса
def update_table(tree, measurements):
    """Обновляет таблицу с измерениями."""
    for item in tree.get_children():
        tree.delete(item)  # Очищаем таблицу
    for measurement in measurements:
        tree.insert("", "end", values=(str(measurement),))


def add_measurement(tree, measurements, entry_type, entry_date, entry_place,
                    entry_value1, entry_value2):
    """Добавляет новое измерение в список и обновляет таблицу."""
    measurement_type = entry_type.get()
    date = entry_date.get()
    place = f'"{entry_place.get()}"'  # Добавляем кавычки для совместимости
    value1 = entry_value1.get()
    value2 = entry_value2.get()

    try:
        if measurement_type == "temperature":
            line = f"temperature {date} {place} {value1} {value2}"
        else:
            line = f"pressure {date} {place} {value1}"
        measurement = parse_line(line)
        measurements.append(measurement)
        update_table(tree, measurements)
    except ValueError:
        print("Ошибка в данных!")


def delete_selected(tree, measurements):
    """Удаляет выделенное измерение из списка и таблицы."""
    selected = tree.selection()
    if selected:
        # Находим индекс выделенного элемента
        for item in selected:
            index = tree.index(item)
            measurements.pop(index)
            tree.delete(item)


# Создание интерфейса
def create_interface(measurements):
    """Создаёт и запускает оконный интерфейс."""
    window = tk.Tk()
    window.title("Измерения")
    window.geometry("600x400")

    # Таблица
    tree = ttk.Treeview(window, columns=("Измерение",), show="headings")
    tree.heading("Измерение", text="Данные измерения")
    tree.pack(fill="both", expand=True)

    # Поля ввода
    frame = tk.Frame(window)
    frame.pack()

    tk.Label(frame, text="Тип:").grid(row=0, column=0)
    entry_type = tk.Entry(frame)
    entry_type.grid(row=0, column=1)

    tk.Label(frame, text="Дата (гггг.мм.дд):").grid(row=0, column=2)
    entry_date = tk.Entry(frame)
    entry_date.grid(row=0, column=3)

    tk.Label(frame, text="Место:").grid(row=1, column=0)
    entry_place = tk.Entry(frame)
    entry_place.grid(row=1, column=1)

    tk.Label(frame, text="Значение 1:").grid(row=1, column=2)
    entry_value1 = tk.Entry(frame)
    entry_value1.grid(row=1, column=3)

    tk.Label(frame, text="Значение 2:").grid(row=2, column=2)
    entry_value2 = tk.Entry(frame)
    entry_value2.grid(row=2, column=3)

    # Кнопки
    tk.Button(frame, text="Добавить",
              command=lambda: add_measurement(tree, measurements, entry_type,
                                             entry_date, entry_place,
                                             entry_value1, entry_value2)).grid(
        row=3, column=0, columnspan=2)
    tk.Button(frame, text="Удалить",
              command=lambda: delete_selected(tree, measurements)).grid(
        row=3, column=2, columnspan=2)

    # Инициализация таблицы
    update_table(tree, measurements)

    window.mainloop()


# Основная программа
def main():
    """Запускает программу."""
    filename = "measurements.txt"
    measurements = read_measurements_from_file(filename)
    create_interface(measurements)


if __name__ == "__main__":
    main()