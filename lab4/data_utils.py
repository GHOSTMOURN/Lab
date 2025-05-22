import os
import logging
from measurements import TemperatureMeasurement
from model_utils import parse_line

# Настройка логирования
logging.basicConfig(
    filename='errors.log',
    level=logging.WARNING,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def read_measurements_from_file(filename):
    """Читает измерения из файла."""
    measurements = []
    script_dir = os.path.dirname(os.path.abspath(__file__))
    abs_filename = os.path.join(script_dir, filename)

    if not os.path.exists(abs_filename):
        logging.error(f"Файл {abs_filename} не найден!")
        return measurements

    try:
        with open(abs_filename, "r", encoding="utf-8-sig") as file:
            for line in file:
                if line.strip():
                    try:
                        measurement = parse_line(line)
                        measurements.append(measurement)
                    except ValueError as e:
                        logging.warning(f"Ошибка в строке: {line.strip()} — {e}")
    except Exception as e:
        logging.error(f"Ошибка чтения файла: {e}")

    print(f"Прочитано {len(measurements)} измерений.")
    return measurements

def save_measurements_to_file(filename, measurements):
    """Сохраняет измерения в файл."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    abs_filename = os.path.join(script_dir, filename)

    try:
        with open(abs_filename, "w", encoding="utf-8") as file:
            for measurement in measurements:
                if isinstance(measurement, TemperatureMeasurement):
                    file.write(f'temperature {measurement.date.strftime("%Y.%m.%d")} '
                               f'"{measurement.place}" {measurement.temperature} '
                               f'{measurement.humidity}\n')
                else:
                    file.write(f'pressure {measurement.date.strftime("%Y.%m.%d")} '
                               f'"{measurement.place}" {measurement.pressure}\n')
        print(f"Данные сохранены в {abs_filename}")
    except Exception as e:
        logging.error(f"Ошибка сохранения файла: {e}")
