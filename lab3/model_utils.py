from measurements import TemperatureMeasurement, PressureMeasurement

def parse_line(line):
    """Создает объект измерения из строки."""
    parts = line.strip().split()
    if not parts:
        raise ValueError("Пустая строка")
    measurement_type = parts[0]
    if measurement_type == "temperature" and len(parts) == 5:
        return TemperatureMeasurement(parts[1], parts[2], parts[3], parts[4])
    elif measurement_type == "pressure" and len(parts) == 4:
        return PressureMeasurement(parts[1], parts[2], parts[3])
    raise ValueError(f"Некорректный формат строки: {line.strip()}")
