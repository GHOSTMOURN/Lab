import unittest
import tempfile
import os
from measurements import TemperatureMeasurement, PressureMeasurement, Measurement
from commands import process_commands

class TestMeasurement(unittest.TestCase):
    def test_valid_measurement(self):
        m = Measurement("2024.05.22", '"Москва"')
        self.assertEqual(str(m), "Дата: 2024-05-22, Место: Москва")

    def test_invalid_date(self):
        with self.assertRaises(ValueError):
            Measurement("2024-05-22", '"Москва"')

class TestTemperatureMeasurement(unittest.TestCase):
    def test_valid_temperature(self):
        t = TemperatureMeasurement("2024.05.22", '"Казань"', "23.5", "45.1")
        self.assertEqual(round(t.temperature, 1), 23.5)
        self.assertEqual(round(t.humidity, 1), 45.1)

    def test_invalid_temperature(self):
        with self.assertRaises(ValueError):
            TemperatureMeasurement("2024.05.22", '"Казань"', "abc", "45.1")

    def test_invalid_humidity(self):
        with self.assertRaises(ValueError):
            TemperatureMeasurement("2024.05.22", '"Казань"', "23.5", "десять")

class TestPressureMeasurement(unittest.TestCase):
    def test_valid_pressure(self):
        p = PressureMeasurement("2024.05.22", '"Томск"', "760")
        self.assertEqual(round(p.pressure), 760)

    def test_invalid_pressure(self):
        with self.assertRaises(ValueError):
            PressureMeasurement("2024.05.22", '"Томск"', "давление")

class TestCommands(unittest.TestCase):
    def setUp(self):
        self.measurements = [
            TemperatureMeasurement("2024.05.01", '"Москва"', "20", "50"),
            PressureMeasurement("2024.05.02", '"Тула"', "750"),
            TemperatureMeasurement("2024.05.03", '"Сочи"', "15", "80"),
        ]

    def test_add_command(self):
        # создаём файл, записываем туда строку, закрываем — только после этого читаем
        cmd_file = tempfile.NamedTemporaryFile("w+", delete=False, encoding="utf-8")
        cmd_file.write("ADD temperature; 2024.05.04; 25.5; Казань; 55.0\n")
        cmd_file.flush()
        cmd_file.close()

        updated = process_commands(cmd_file.name, self.measurements)
        self.assertEqual(len(updated), 4)
        self.assertIn("Казань", str(updated[-1]))

        os.remove(cmd_file.name)

    def test_rem_command(self):
        cmd_file = tempfile.NamedTemporaryFile("w+", delete=False, encoding="utf-8")
        cmd_file.write("REM temperature < 18\n")
        cmd_file.flush()
        cmd_file.close()

        updated = process_commands(cmd_file.name, self.measurements)
        self.assertEqual(len(updated), 2)

        os.remove(cmd_file.name)

    def test_save_command(self):
        output_file = tempfile.NamedTemporaryFile("w+", delete=False, encoding="utf-8")
        filename = output_file.name
        output_file.close()

        cmd_file = tempfile.NamedTemporaryFile("w+", delete=False, encoding="utf-8")
        cmd_file.write(f"SAVE {filename}\n")
        cmd_file.flush()
        cmd_file.close()

        process_commands(cmd_file.name, self.measurements)

        with open(filename, "r", encoding="utf-8") as f:
            content = f.read()
            self.assertTrue("Москва" in content or "Тула" in content)

        os.remove(cmd_file.name)
        os.remove(filename)

if __name__ == '__main__':
    unittest.main()
