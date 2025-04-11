import datetime  # Импортируем модуль для работы с датами

class Measurement:  # Базовый класс измерений
    def __init__(self, date, place):  # Конструктор класса
        self.date = datetime.datetime.strptime(date, "%Y.%m.%d").date()  # Преобразуем строку с датой в объект datetime
        self.place = place.strip('"')  # Убираем кавычки у названия места
    
    def __str__(self):  # Метод для строкового представления объекта
        return f"Дата: {self.date}, Место: {self.place}"  # Возвращаем строку с датой и местом измерения

class TemperatureMeasurement(Measurement):  # Класс для измерения температуры, наследуемый от Measurement
    def __init__(self, date, place, temperature, humidity):  # Конструктор
        super().__init__(date, place)  # Вызываем конструктор родительского класса
        self.temperature = float(temperature)  # Преобразуем температуру в число
        self.humidity = float(humidity)  # Преобразуем влажность в число
    
    def __str__(self):  # Переопределяем метод строкового представления
        return (super().__str__() +  # Вызываем родительский метод __str__ для даты и места
                f", Температура: {self.temperature:.2f}°C, Влажность: {self.humidity:.2f}%")  # Добавляем данные о температуре и влажности

class PressureMeasurement(Measurement):  # Класс для измерения давления, наследуемый от Measurement
    def __init__(self, date, place, pressure):  # Конструктор
        super().__init__(date, place)  # Вызываем конструктор родительского класса
        self.pressure = float(pressure)  # Преобразуем давление в число
    
    def __str__(self):  # Переопределяем метод строкового представления
        return (super().__str__() +  # Вызываем родительский метод __str__ для даты и места
                f", Давление: {self.pressure:.2f} мм рт. ст.")  # Добавляем данные о давлении

def parse_input(input_str):  # Функция для обработки ввода пользователя
    parts = input_str.split()  # Разбиваем строку на части по пробелам
    type_of_measurement = parts[0]  # Первый параметр - тип измерения (temperature или pressure)
    
    if type_of_measurement == "temperature":  # Если ввод относится к температуре
        return TemperatureMeasurement(parts[1], parts[2], parts[3], parts[4])  # Создаем объект TemperatureMeasurement
    elif type_of_measurement == "pressure":  # Если ввод относится к давлению
        return PressureMeasurement(parts[1], parts[2], parts[3])  # Создаем объект PressureMeasurement
    else:
        raise ValueError("Неизвестный тип измерения")  # Если введен неизвестный тип, вызываем ошибку

# Создаем список для хранения объектов измерений
measurements = []  # Контейнер для хранения всех объектов

# Запрашиваем у пользователя данные для первого измерения (температура и влажность)
input_data1 = input("Введите данные (temperature гггг.мм.дд \"место\" температура влажность): ")  # Получаем ввод от пользователя
measurements.append(parse_input(input_data1))  # Обрабатываем ввод и добавляем объект в список

# Запрашиваем у пользователя данные для второго измерения (давление)
input_data2 = input("Введите данные (pressure гггг.мм.дд \"место\" давление): ")  # Получаем ввод от пользователя
measurements.append(parse_input(input_data2))  # Обрабатываем ввод и добавляем объект в список

# Выводим все измерения
for measurement in measurements:  # Перебираем все объекты в списке
    print(measurement)  # Вызываем __str__() для каждого объекта (полиморфизм) и выводим данные