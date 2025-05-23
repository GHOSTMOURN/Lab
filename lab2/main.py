from data_utils import read_measurements_from_file
from gui_utils import create_interface
from measurements import fu

def main():
    """Запускает программу."""
    filename = "measurements.txt"  # Файл в D:\CODE\Python\Labi
    measurements = read_measurements_from_file(filename)
    avg = fu.average_temperature(measurements)
    print("Средняя температура", round(avg, 2), "C")
    create_interface(measurements, filename)

if __name__ == "__main__":
    main()