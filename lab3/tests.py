import unittest
from measurements import TemperatureMeasurement, PressureMeasurement, Measurement

class TestMeasurement(unittest.TestCase):
    def test_valid_measurement(self):
        m = Measurement("2024.05.22", '"Москва"')
        self.assertEqual(str(m), "Дата: 2024-05-22, Место: Москва")

    def test_invalid_date(self):
        with self.assertRaises(ValueError):
            Measurement("2024-05-22", '"Москва"')  # неправильный формат даты

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

if __name__ == '__main__':
    unittest.main()