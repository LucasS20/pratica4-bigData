import os
import unittest
from dataProcessor import read_json_file, avg_age_country,country_frequency,oldest_person_per_country


class TestDataProcessor(unittest.TestCase):
    def test_read_json_file_success(self):
        current_directory = os.path.dirname(__file__)
        file_path = os.path.join(current_directory, "../users.json")

        data = read_json_file(file_path)

        self.assertEqual(len(data), 1000)  # Ajustar o número esperado de registros
        self.assertEqual(data[0]['name'], 'Charles Martin')
        self.assertEqual(data[1]['age'], 56)

    def test_read_json_file_file_not_found(self):
        with self.assertRaises(FileNotFoundError):
            read_json_file("non_existent.json")

    def test_read_json_file_invalid_json(self):
        with open("invalid.json", "w") as file:
            file.write("invalid json data")
        with self.assertRaises(ValueError):
            read_json_file("invalid.json")

    def test_avgAgeCountry_empty_json(self):
        data = []
        result = avg_age_country(data)
        self.assertEqual(result, {})

    def test_avgAgeCountry_missing_age(self):
        data = [{"name": "Charles Martin", "country": "JP"}]
        result = avg_age_country(data)
        self.assertEqual(result, {"JP": None})

    def test_avgAgeCountry_missing_country(self):
        data = [{"name": "Charles Martin", "age": 28}]
        result = avg_age_country(data)
        self.assertEqual(result, {})

    def test_avgAgeCountry_transform_fn(self):
        data = [{"name": "Charles Martin", "age": 28, "country": "JP"}]
        result = avg_age_country(data, lambda x: x * 12)
        self.assertEqual(result, {"JP": 28 * 12})

    def test_avgAgeCountry_all_ages_none(self):
        data = [{"name": "Charles Martin", "age": None, "country": "JP"},
                {"name": "Ashley Neal", "age": None, "country": "JP"}]
        result = avg_age_country(data)
        self.assertEqual(result, {"JP": None})

    def test_avgAgeCountry_some_ages_none(self):
        data = [{"name": "Charles Martin", "age": 28, "country": "JP"},
                {"name": "Ashley Neal", "age": None, "country": "JP"}]
        result = avg_age_country(data)
        self.assertEqual(result, {"JP": 28})

    def test_avgAgeCountry_transform_fn_with_none(self):
        data = [{"name": "Charles Martin", "age": 28, "country": "JP"},
                {"name": "Ashley Neal", "age": None, "country": "JP"}]
        result = avg_age_country(data, lambda x: x * 12 if x is not None else None)
        self.assertEqual(result, {"JP": 28 * 12})

    def test_avgAgeCountry_multiple_countries(self):
        data = [{"name": "Charles Martin", "age": 28, "country": "JP"},
                {"name": "Ashley Neal", "age": 56, "country": "US"}]
        result = avg_age_country(data)
        self.assertEqual(result, {"JP": 28, "US": 56})

    def test_country_frequency(self):
        data = [{"name": "Charles Martin", "age": 28, "country": "JP"},
                {"name": "Ashley Neal", "age": 56, "country": "US"},
                {"name": "John Doe", "age": 34, "country": "JP"}]
        result = country_frequency(data)
        self.assertEqual(result, {"JP": 2, "US": 1})

    def test_oldest_person_per_country(self):
        data = [{"name": "Charles Martin", "age": 28, "country": "JP"},
                {"name": "Ashley Neal", "age": 56, "country": "US"},
                {"name": "John Doe", "age": 34, "country": "JP"}]
        result = oldest_person_per_country(data)
        self.assertEqual(result, {"JP": {"name": "John Doe", "age": 34, "country": "JP"},
                                  "US": {"name": "Ashley Neal", "age": 56, "country": "US"}})


if __name__ == '__main__':
    unittest.main()
