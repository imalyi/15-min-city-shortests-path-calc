import json
from database import MongoDatabase


def read_categories():
    #NOT WORKING
    categories = set()
    with open("data.json", "r", encoding="utf8") as f:
        data = json.loads(f.read())
    for line in data:
        for category in line.get('categories'):
            categories.add(category)
    return categories


def get_categories() -> dict:
    with open("categories.json", "r") as f:
        data = json.loads(f.read())
    clean_data = {}
    for main_category, sub_category in data.items():
        clean_data[main_category] = list(sub_category.keys())
    return clean_data


def generate_dict_with_empty_categories() -> dict:
    categories_structure = {}
    categories = get_categories()
    for main_category, sub_categories in categories.items():
        for sub_category in sub_categories:
            if not categories_structure.get(main_category):
                categories_structure[main_category] = {}
            if not categories_structure[main_category].get(sub_category):
                categories_structure[main_category][sub_category] = []
    return categories_structure


def save():
    db = MongoDatabase()
    db.insert_categories(get_categories())

save()