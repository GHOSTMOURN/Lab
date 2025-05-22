import logging
from model_utils import parse_line
from data_utils import save_measurements_to_file

logging.basicConfig(
    filename='errors.log',
    level=logging.WARNING,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def process_commands(filename, measurements):
    """
    Выполняет команды из файла.
    Доступные команды:
    - ADD <данные>
    - REM <условие>
    - SAVE <имя_файла>
    """
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            for line in f:
                if not line.strip():
                    continue
                try:
                    print("Команда из файла:", repr(line.strip()))
                    print("Строка:", repr(line))
                    if line.startswith("ADD "):
                        data_part = line[4:].strip()
                        parts = [p.strip() for p in data_part.split(";")]

                        if len(parts) == 5 and parts[0] == "temperature":
                            line_str = f'temperature {parts[1]} "{parts[3]}" {parts[2]} {parts[4]}'
                        elif len(parts) == 4 and parts[0] == "pressure":
                            line_str = f'pressure {parts[1]} "{parts[3]}" {parts[2]}'
                        else:
                            raise ValueError(f"Некорректный формат строки ADD: {data_part}")

                        print("Собранная строка для parse_line:", repr(line_str))
                        measurement = parse_line(line_str)
                        measurements.append(measurement)

                    elif line.startswith("REM "):
                        condition = line[4:].strip()
                        measurements[:] = apply_rem_condition(measurements, condition)

                    elif line.startswith("SAVE "):
                        save_file = line[5:].strip()
                        save_measurements_to_file(save_file, measurements)

                except Exception as e:
                    logging.warning(f"Ошибка при выполнении команды '{line.strip()}': {e}")

        return measurements

    except Exception as e:
        logging.error(f"Не удалось прочитать файл с командами: {e}")
        return measurements

def apply_rem_condition(measurements, condition):
    """
    Удаляет объекты по условию, например:
    REM temperature < 18
    REM humidity > 50
    """
    try:
        field, operator, value = condition.split()
        value = float(value)
    except Exception as e:
        logging.warning(f"Ошибка разбора условия REM: {condition} — {e}")
        return measurements

    def matches(obj):
        attr = getattr(obj, field, None)
        if attr is None:
            return False
        try:
            attr = float(attr)
        except:
            return False

        if operator == "<":
            return attr < value
        elif operator == ">":
            return attr > value
        elif operator == "==":
            return attr == value
        return False

    return [m for m in measurements if not matches(m)]
