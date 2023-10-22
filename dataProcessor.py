from collections import defaultdict
import json


def read_json_file(file_path):
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
            return data
    except FileNotFoundError:
        raise FileNotFoundError(f"File not found: {file_path}")
    except json.JSONDecodeError:
        raise ValueError(f"Invalid JSON format in file: {file_path}")


def avg_age_country(data, transform_fn=None):
    country_age = defaultdict(list)
    for person in data:
        if 'country' in person:
            age = person.get('age')
            if age is not None and transform_fn:
                age = transform_fn(age)
            country_age[person['country']].append(age)

    avg_age = {}
    for country, ages in country_age.items():
        ages = [age for age in ages if age is not None]
        avg_age[country] = sum(ages) / len(ages) if ages else None

    return avg_age
