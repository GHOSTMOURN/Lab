import datetime

class Measurement:
    """Базовый класс для хранения данных об измерении."""
    def __init__(self, date, place):
        try:
            self.date = datetime.datetime.strptime(date, "%Y.%m.%d").date()
        except ValueError:
            raise ValueError(f"Неверный формат даты: {date} (нужен формат гггг.мм.дд)")
        self.place = place.strip('"')

    def __str__(self):
        return f"Дата: {self.date}, Место: {self.place}"

class TemperatureMeasurement(Measurement):
    """Класс для измерения температуры и влажности."""
    def __init__(self, date, place, temperature, humidity):
        super().__init__(date, place)
        try:
            self.temperature = float(temperature)
        except ValueError:
            raise ValueError(f"Температура должна быть числом: {temperature}")
        try:
            self.humidity = float(humidity)
        except ValueError:
            raise ValueError(f"Влажность должна быть числом: {humidity}")

    def __str__(self):
        return (f"{super().__str__()}, "
                f"Температура: {self.temperature:.2f}°C, "
                f"Влажность: {self.humidity:.2f}%")

class PressureMeasurement(Measurement):
    """Класс для измерения давления."""
    def __init__(self, date, place, pressure):
        super().__init__(date, place)
        try:
            self.pressure = float(pressure)
        except ValueError:
            raise ValueError(f"Давление должно быть числом: {pressure}")

    def __str__(self):
        return f"{super().__str__()}, Давление: {self.pressure:.2f} мм рт. ст."
