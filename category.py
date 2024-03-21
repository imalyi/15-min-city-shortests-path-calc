import json
from database import MongoDatabase


def read_categories():
    categories = set()
    with open("data.json", "r", encoding="utf8") as f:
        data = json.loads(f.read())
    for line in data:
        for category in line.get('categories'):
            categories.add(category)
    return categories


def get_categories():
    with open("categories.json", "r") as f:
        data = json.loads(f.read())
    clean_data = {}
    for main_category, sub_category in data.items():
        clean_data[main_category] = list(sub_category.keys())
    return clean_data


def save():
    db = MongoDatabase()
    db.insert_categories(get_categories())

